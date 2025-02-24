import { Worker } from '@temporalio/worker';
import { findEligiblePartner } from './activities';

async function run() {
  const worker = await Worker.create({
    activities: {
      findEligiblePartner,
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