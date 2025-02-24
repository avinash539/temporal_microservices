"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const worker_1 = require("@temporalio/worker");
const activities_1 = require("./activities");
async function run() {
    const worker = await worker_1.Worker.create({
        activities: {
            distributeOrder: activities_1.distributeOrder,
        },
        taskQueue: 'create-manifest',
    });
    console.log('Distributor service worker started, listening to task queue: distributor-service');
    await worker.run();
}
run().catch((err) => {
    console.error('Error running distributor service worker:', err);
    process.exit(1);
});
