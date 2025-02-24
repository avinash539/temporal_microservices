"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const worker_1 = require("@temporalio/worker");
// import * as workflows from './workflows';
// import * as manifestationWorkflow from './manifestation-workflow';
async function run() {
    const worker = await worker_1.Worker.create({
        workflowsPath: require.resolve('./workflows'),
        // workflowsPath: require.resolve('./manifestation-workflow'),
        taskQueue: 'new-order-task-queue',
    });
    console.log('Worker started, listening to task queue: bigship-manifest-order-task-queue');
    await worker.run();
}
run().catch((err) => {
    console.error('Error running worker:', err);
    process.exit(1);
});
