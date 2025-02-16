import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shared.update_workflow import ShipmentTrackingWorkflow
from shared.constants import TRACKING_UPDATE_TASK_QUEUE

async def main():
    client = await Client.connect("localhost:7233")
    
    # Run the worker
    worker = Worker(
        client,
        task_queue=TRACKING_UPDATE_TASK_QUEUE,
        workflows=[ShipmentTrackingWorkflow],
    )
    
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 