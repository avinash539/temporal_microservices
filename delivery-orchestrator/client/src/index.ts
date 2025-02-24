import { Client } from '@temporalio/client';

interface OrderManifestationDetails {
    awbNumber: string;
    systemOrderId: number;
    courierId: number;
    riskType: string;
}

async function run() {
    const client = new Client();

    // Example 1: Order with predefined partner
    const orderManifestationDetails: OrderManifestationDetails = {
        awbNumber: '12345',
        systemOrderId: 1002651866,
        courierId: 15,
        riskType: 'OwnerRisk'
    };

    try {
        // Start workflow for order with partner
        const handle1 = await client.workflow.start('orderManifestationWorkflow', {
            args: [orderManifestationDetails],
            taskQueue: 'bigship-manifest-order-task-queue',
            workflowId: `bigship-manifest-order-${orderManifestationDetails.awbNumber}`,
        });
        console.log(`Started workflow for order with partner: ${handle1.workflowId}`);


        // Wait for both workflows to complete
        await Promise.all([
            handle1.result(),
        ]);
        console.log('Workflows completed successfully');

    } catch (err) {
        console.error('Error running workflows:', err);
        process.exit(1);
    }
}

run().catch((err) => {
    console.error('Error in client:', err);
    process.exit(1);
});