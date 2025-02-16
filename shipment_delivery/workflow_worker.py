import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shipment_delivery.shared.constants import WORKFLOW_TASK_QUEUE
from shipment_delivery.shared.workflow import ShipmentDeliveryWorkflow

async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233", namespace="default")
    
    # Run the worker
    worker = Worker(
        client,
        task_queue=WORKFLOW_TASK_QUEUE,
        workflows=[ShipmentDeliveryWorkflow]
    )
    
    print(f"Starting workflow worker on task queue: {WORKFLOW_TASK_QUEUE}")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 