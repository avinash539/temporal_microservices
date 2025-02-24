"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const client_1 = require("@temporalio/client");
async function run() {
    const client = new client_1.Client();
    // Example 1: Order with predefined partner
    const orderManifestationDetails = {
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
    }
    catch (err) {
        console.error('Error running workflows:', err);
        process.exit(1);
    }
}
run().catch((err) => {
    console.error('Error in client:', err);
    process.exit(1);
});
