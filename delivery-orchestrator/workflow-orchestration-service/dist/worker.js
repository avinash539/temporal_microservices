"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const worker_1 = require("@temporalio/worker");
async function run() {
    const worker = await worker_1.Worker.create({
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
