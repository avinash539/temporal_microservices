"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const worker_1 = require("@temporalio/worker");
const activities_1 = require("./activities");
async function run() {
    const worker = await worker_1.Worker.create({
        activities: {
            findEligiblePartner: activities_1.findEligiblePartner,
        },
        taskQueue: 'create-manifest',
    });
    console.log('Atlas service worker started, listening to task queue: atlas-service');
    await worker.run();
}
run().catch((err) => {
    console.error('Error running Atlas service worker:', err);
    process.exit(1);
});
