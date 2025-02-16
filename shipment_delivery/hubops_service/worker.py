import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.service import RPCError
from shipment_delivery.shared.constants import HUBOPS_TASK_QUEUE
from .activities import HubOpsService

# Constants for resume signal
WORKFLOW_ID = "shipment-delivery-3a012a6f-1036-4ed0-b8ce-a9a93bb6c8e7"  # Replace with your actual workflow ID pattern
SIGNAL_NAME = "resume_service"
SERVICE_NAME = "HubOps Service"  # Match the name used in the workflow

async def send_resume_signal(client: Client) -> None:
    """Send resume signal to any paused workflow that might be waiting for HubOps service"""
    try:
        # You might want to handle multiple workflows by listing and filtering them
        # For now, we'll just signal a specific workflow
        workflow_handle = client.get_workflow_handle(WORKFLOW_ID)
        await workflow_handle.signal(SIGNAL_NAME, SERVICE_NAME)
        print(f"Sent resume signal to workflow {WORKFLOW_ID}")
    except Exception as e:
        print(f"Failed to send resume signal: {str(e)}")
        # Don't raise the exception - we want the worker to start even if signal fails
        
async def send_resume_signal_to_all_workflows(client: Client) -> None:
    """Send resume signal to all running workflows that might be waiting for HubOps service"""
    try:
        print("Checking for paused workflows...")
        # List only running workflows
        async for workflow in client.list_workflows(
            # Only get workflows from our shipment delivery service
            query="WorkflowType='ShipmentDeliveryWorkflow' AND ExecutionStatus='Running'"
        ):
            try:
                # Get handle for each workflow
                handle = client.get_workflow_handle(workflow.id)
                # Try to send resume signal
                await handle.signal(SIGNAL_NAME, SERVICE_NAME)
                print(f"✓ Sent resume signal to workflow {workflow.id}")
            except RPCError as e:
                if "workflow execution not found" in str(e).lower():
                    # This shouldn't happen since we're filtering for running workflows
                    continue
                print(f"! Failed to signal workflow {workflow.id}: {str(e)}")
            except Exception as e:
                print(f"! Error signaling workflow {workflow.id}: {str(e)}")
    except Exception as e:
        print(f"! Failed to list workflows: {str(e)}")
    else:
        print("Finished checking workflows")

async def main() -> None:
    # Connect to temporal server
    client = await Client.connect("localhost:7233", namespace="default")
    
    # First, try to resume any paused workflows
    # await send_resume_signal(client)
    await send_resume_signal_to_all_workflows(client)
    
    # Run the worker
    service = HubOpsService()
    worker = Worker(
        client,
        task_queue=HUBOPS_TASK_QUEUE,
        activities=[service.process_hub_operations],
    )
    print("\nStarting hub operations service worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 