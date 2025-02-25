import { Worker } from '@temporalio/worker';
import { distributeOrder, attemptPartnerDistribution } from './activities';

async function run() {
  const worker = await Worker.create({
    activities: {
      distributeOrder,
      attemptPartnerDistribution,
    },
    taskQueue: 'distributor-service-task-queue',
  });

  console.log('Distributor service worker started, listening to task queue: distributor-service-task-queue');
  await worker.run();
}

run().catch((err) => {
  console.error('Error running distributor service worker:', err);
  process.exit(1);
});