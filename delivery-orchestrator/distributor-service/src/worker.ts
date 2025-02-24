import { Worker } from '@temporalio/worker';
import { distributeOrder } from './activities';

async function run() {
  const worker = await Worker.create({
    activities: {
      distributeOrder,
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