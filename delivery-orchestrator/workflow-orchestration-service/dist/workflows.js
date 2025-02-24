"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.orderDeliveryWorkflow = orderDeliveryWorkflow;
const workflow_1 = require("@temporalio/workflow");
// const { findEligiblePartner, distributeOrder } = proxyActivities<Activities>({
//     startToCloseTimeout: '1 minute',
// });
const { findEligiblePartner } = (0, workflow_1.proxyActivities)({
    startToCloseTimeout: '1 minute',
    taskQueue: 'atlas-service-task-queue',
    retry: {
        maximumAttempts: 3,
        backoffCoefficient: 2,
    }
});
const { distributeOrder } = (0, workflow_1.proxyActivities)({
    startToCloseTimeout: '1 minute',
    taskQueue: 'distributor-service-task-queue',
    retry: {
        maximumAttempts: 3,
        backoffCoefficient: 2,
    }
});
// Define the retry signal
const retryActivitySignal = (0, workflow_1.defineSignal)('retryActivity');
async function orderDeliveryWorkflow(orderData) {
    let partner;
    let retrySignalReceived = false;
    let retryAttempts = 0;
    const MAX_RETRY_ATTEMPTS = 3;
    // Set up signal handler for retry
    (0, workflow_1.setHandler)(retryActivitySignal, () => {
        console.log('Retry signal received');
        retrySignalReceived = true;
    });
    while (!partner && retryAttempts < MAX_RETRY_ATTEMPTS) {
        try {
            if (orderData.partnerId) {
                // Scenario 1: Order already has a partner assigned
                partner = {
                    partnerId: orderData.partnerId,
                    name: 'predefined-partner',
                    config: {}
                };
            }
            else {
                // Scenario 2: Need to find eligible partner through Atlas service
                partner = await findEligiblePartner(orderData);
            }
        }
        catch (error) {
            retryAttempts++;
            console.log(`Activity failed, attempt ${retryAttempts} of ${MAX_RETRY_ATTEMPTS}`);
            if (retryAttempts < MAX_RETRY_ATTEMPTS) {
                // Wait for retry signal with a timeout
                const signalTimeout = 300; // 5 minutes in seconds
                let timeWaited = 0;
                while (!retrySignalReceived && timeWaited < signalTimeout) {
                    await (0, workflow_1.sleep)('1 second');
                    timeWaited++;
                }
                if (!retrySignalReceived) {
                    console.log('No retry signal received within timeout, continuing to next attempt');
                }
                // Reset signal flag for next attempt
                retrySignalReceived = false;
            }
        }
    }
    if (partner) {
        await distributeOrder(orderData, partner);
    }
    else {
        throw new Error(`Failed to find eligible partner after ${MAX_RETRY_ATTEMPTS} attempts`);
    }
}
