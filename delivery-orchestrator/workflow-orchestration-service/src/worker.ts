import { Worker } from '@temporalio/worker';
import * as workflows from './workflows';

async function run() {
    const worker = await Worker.create({
        workflowsPath: require.resolve('./workflows'),
        taskQueue: 'create-manifest',
    });

    console.log('Worker started, listening to task queue: order-delivery');
    await worker.run();
}

run().catch((err) => {
    console.error('Error running worker:', err);
    process.exit(1);
});