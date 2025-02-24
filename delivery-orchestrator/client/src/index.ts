import { Client } from '@temporalio/client';

interface OrderData {
    orderId: string;
    partnerId?: string;
    orderDetails: Record<string, any>;
}

async function run() {
    const client = new Client();

    // Example 1: Order with predefined partner
    const orderWithPartner: OrderData = {
        orderId: 'order-112',
        partnerId: 'partner-xyz',
        orderDetails: {
            items: [
                { name: 'Product 1', quantity: 2 }
            ],
            deliveryAddress: '123 Main St, City'
        }
    };

    // Example 2: Order without partner (needs partner discovery)
    const orderWithoutPartner: OrderData = {
        orderId: 'order-113',
        orderDetails: {
            items: [
                { name: 'Product 2', quantity: 1 }
            ],
            deliveryAddress: '456 Oak St, City'
        }
    };

    try {
        // Start workflow for order with partner
        const handle1 = await client.workflow.start('orderDeliveryWorkflow', {
            args: [orderWithPartner],
            taskQueue: 'create-manifest',
            workflowId: `delivery-${orderWithPartner.orderId}`,
        });
        console.log(`Started workflow for order with partner: ${handle1.workflowId}`);

        // Start workflow for order without partner
        const handle2 = await client.workflow.start('orderDeliveryWorkflow', {
            args: [orderWithoutPartner],
            taskQueue: 'create-manifest',
            workflowId: `delivery-${orderWithoutPartner.orderId}`,
        });
        console.log(`Started workflow for order without partner: ${handle2.workflowId}`);

        // Wait for both workflows to complete
        await Promise.all([
            handle1.result(),
            handle2.result()
        ]);
        console.log('Both workflows completed successfully');

    } catch (err) {
        console.error('Error running workflows:', err);
        process.exit(1);
    }
}

run().catch((err) => {
    console.error('Error in client:', err);
    process.exit(1);
});