import { proxyActivities } from '@temporalio/workflow';

interface OrderManifestationDetails {
    awbNumber: string;
    systemOrderId: number;
    courierId: number;
    riskType: string;
}

interface ManifestationResponse {
    statusCode: number;
    message: string;
    data: any;
}

interface Activities {
    bigshipOrderManifestationActivity: (orderManifestationData: OrderManifestationDetails) => Promise<ManifestationResponse>;
}

const { bigshipOrderManifestationActivity } = proxyActivities<Activities>({
    startToCloseTimeout: '1 minute',
    taskQueue: 'distributor-service-task-queue'
});

export async function orderManifestationWorkflow(orderManifestationData: OrderManifestationDetails): Promise<ManifestationResponse> {
    const response = await bigshipOrderManifestationActivity(orderManifestationData);

    if (response.statusCode === 200) {
        // Both success and expected failure cases should complete the workflow
        return response; // This will complete the workflow
    }

    // For any other status code, throw an error
    throw new Error(`Manifestation failed: ${response.message}`);
}