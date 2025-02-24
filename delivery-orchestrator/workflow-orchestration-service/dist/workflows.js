"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.orderDeliveryWorkflow = orderDeliveryWorkflow;
const workflow_1 = require("@temporalio/workflow");
const { findEligiblePartner, distributeOrder } = (0, workflow_1.proxyActivities)({
    startToCloseTimeout: '1 minute',
});
// const { findEligiblePartner } = proxyActivities<Activities>({startToCloseTimeout: '1 minute', taskQueue: 'atlas-service'});
// const { distributeOrder } = proxyActivities<Activities>({startToCloseTimeout: '1 minute', taskQueue: 'distributor-service'});
async function orderDeliveryWorkflow(orderData) {
    let partner;
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
    // Distribute order to the partner
    await distributeOrder(orderData, partner);
}
