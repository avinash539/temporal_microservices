import { Worker } from '@temporalio/worker';
import { Client, WorkflowClient } from '@temporalio/client';
import { findEligiblePartner } from './activities';

async function sendResumeSignalToFieldTasks() {
  const client = new Client();

  try {
    console.log('Scanning for failed workflows that need retry...');

    // Get all failed workflows of type orderDeliveryWorkflow that are still active
    const result = await client.workflow.list({
      query: 'WorkflowType="orderDeliveryWorkflow" AND ExecutionStatus="Failed" AND CloseTime IS NULL'
    });

    let retryCount = 0;
    let errorCount = 0;

    for await (const workflow of result) {
      try {
        // Check if workflow is still accessible before sending signal
        const handle = client.workflow.getHandle(workflow.workflowId);

        // Send retry signal
        await handle.signal('retryActivity');
        retryCount++;
        console.log(`✓ Successfully sent retry signal to workflow ${workflow.workflowId}`);
      } catch (error) {
        errorCount++;
        console.error(`✗ Failed to send signal to workflow ${workflow.workflowId}:`, error);
      }
    }

    console.log(`Retry operation completed:\n- Successfully sent signals: ${retryCount}\n- Failed to send signals: ${errorCount}`);
  } catch (error) {
    console.error('Critical error while listing workflows:', error);
    // Don't throw the error to allow worker to start
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
  // console.log('Initializing retry mechanism for failed workflows...');
  // await sendResumeSignalToFieldTasks();

  // Start the worker
  console.log('Starting Atlas service worker...');
  await worker.run();
}

run().catch((err) => {
  console.error('Fatal error in Atlas service worker:', err);
  process.exit(1);
});