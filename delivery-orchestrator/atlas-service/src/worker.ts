import { Worker } from '@temporalio/worker';
import { Client, WorkflowClient } from '@temporalio/client';
import { findEligiblePartner } from './activities';

async function sendResumeSignalToFieldTasks() {
  const client = new Client();

  try {
    // Get all failed workflows of type orderDeliveryWorkflow
    const result = await client.workflow.list({
      query: 'WorkflowType="orderDeliveryWorkflow" AND ExecutionStatus="FAILED"'
    });

    console.log('Checking for failed workflows to retry...');

    for await (const workflow of result) {
      try {
        const handle = client.workflow.getHandle(workflow.workflowId);

        // Send retry signal
        await handle.signal('retryActivity');
        console.log(`Sent retry signal to workflow ${workflow.workflowId}`);
      } catch (error) {
        console.error(`Failed to send signal to workflow ${workflow.workflowId}:`, error);
      }
    }
  } catch (error) {
    console.error('Error listing workflows:', error);
  }
}

async function run() {
  const worker = await Worker.create({
    activities: {
      findEligiblePartner,
    },
    taskQueue: 'atlas-service-task-queue',
  });

  // Send signals to failed workflows on startup
  await sendResumeSignalToFieldTasks();

  // Start the worker
  console.log('Starting Atlas service worker...');
  await worker.run();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});