import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shipment_delivery.shared.constants import TRACKING_TASK_QUEUE
from shipment_delivery.tracking_service.activities import TrackingService

async def main() -> None:
    client = await Client.connect("localhost:7233", namespace="default")
    
    # Run the worker
    service = TrackingService()
    worker = Worker(
        client,
        task_queue=TRACKING_TASK_QUEUE,
        activities=[service.update_tracking],
    )
    print("Starting tracking service worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 