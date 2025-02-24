import { proxyActivities } from '@temporalio/workflow';

interface OrderData {
    orderId: string;
    partnerId?: string;
    orderDetails: Record<string, any>;
}

interface NetworkPartner {
    partnerId: string;
    name: string;
    config: Record<string, any>;
}

interface Activities {
    findEligiblePartner: (orderData: OrderData) => Promise<NetworkPartner>;
    distributeOrder: (orderData: OrderData, partner: NetworkPartner) => Promise<void>;
}

// const { findEligiblePartner, distributeOrder } = proxyActivities<Activities>({
//     startToCloseTimeout: '1 minute',
// });
const { findEligiblePartner } = proxyActivities<Activities>({
    startToCloseTimeout: '1 minute',
    taskQueue: 'atlas-service-task-queue',
    retry: {
        maximumAttempts: 3,
        backoffCoefficient: 2,
    }
});
const { distributeOrder } = proxyActivities<Activities>({
    startToCloseTimeout: '1 minute',
    taskQueue: 'distributor-service-task-queue',
    retry: {
        maximumAttempts: 3,
        backoffCoefficient: 2,
    }
});

export async function orderDeliveryWorkflow(orderData: OrderData): Promise<void> {
    let partner: NetworkPartner;

    if (orderData.partnerId) {
        // Scenario 1: Order already has a partner assigned
        partner = {
            partnerId: orderData.partnerId,
            name: 'predefined-partner',
            config: {}
        };
    } else {
        // Scenario 2: Need to find eligible partner through Atlas service
        partner = await findEligiblePartner(orderData);
    }

    // Distribute order to the partner
    await distributeOrder(orderData, partner);
}