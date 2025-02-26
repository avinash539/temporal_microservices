import { proxyActivities } from '@temporalio/workflow';

// Define the interfaces locally to avoid import path issues
interface OrderData {
    orderId: string;
    partnerId?: string;
    orderDetails: {
        items: Array<{ name: string; quantity: number }>;
        deliveryAddress: string;
    };
}

interface Partner {
    partnerId: string;
    name: string;
    config: {
        apiEndpoint: string;
        region: string;
    };
    priority: number;
}

interface DistributionResult {
    success: boolean;
    partnerId: string;
    partnerName: string;
    orderId: string;
    attemptNumber: number;
    totalAttempts: number;
}

interface Activities {
    findEligiblePartner: (orderData: OrderData) => Promise<Partner[]>;
    attemptPartnerDistribution: (
        orderData: OrderData,
        partner: Partner,
        attemptNumber: number,
        totalAttempts: number,
        retryAttempt: number
    ) => Promise<DistributionResult>;
}

const { findEligiblePartner } = proxyActivities<Activities>({
    startToCloseTimeout: '60 seconds',
    taskQueue: 'atlas-service-task-queue',
    retry: {
        maximumAttempts: 5,
        backoffCoefficient: 2,
    }
});

const { attemptPartnerDistribution } = proxyActivities<Activities>({
    startToCloseTimeout: '60 seconds',
    taskQueue: 'distributor-service-task-queue',
    retry: {
        maximumAttempts: 3,
        backoffCoefficient: 30,
    }
});

const MAX_RETRIES_PER_PARTNER = 1;

export async function orderDeliveryWorkflow(orderData: OrderData): Promise<DistributionResult> {
    // Get eligible delivery partners
    const partners = await findEligiblePartner(orderData);

    // Try each partner in sequence
    for (let i = 0; i < partners.length; i++) {
        const partner = partners[i];
        const partnerAttemptNumber = i + 1;

        // Try this partner up to MAX_RETRIES_PER_PARTNER times
        for (let retryAttempt = 1; retryAttempt <= MAX_RETRIES_PER_PARTNER; retryAttempt++) {
            try {
                // Attempt distribution with this partner
                const result = await attemptPartnerDistribution(
                    orderData,
                    partner,
                    partnerAttemptNumber,
                    partners.length,
                    retryAttempt
                );

                // If successful, return the result
                return result;
            } catch (error) {
                // If we haven't exhausted retries for this partner, continue to next retry
                if (retryAttempt < MAX_RETRIES_PER_PARTNER) {
                    continue;
                }

                // If we've exhausted retries for this partner
                if (i === partners.length - 1) {
                    // If this was the last partner, throw the error
                    throw new Error(
                        `All partners failed. Last partner ${partner.name} failed after ${MAX_RETRIES_PER_PARTNER} attempts. Error: ${error instanceof Error ? error.message : 'Unknown error'}`
                    );
                }
                // Move to next partner
                break;
            }
        }
    }

    // This should never be reached due to the error handling above
    throw new Error('No partners available to process the order');
}