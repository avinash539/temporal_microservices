import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shipment_delivery.shared.constants import DRS_TASK_QUEUE
from shipment_delivery.drs_service.activities import DRSService

async def main() -> None:
    client = await Client.connect("localhost:7233", namespace="default")
    
    # Run the worker
    service = DRSService()
    worker = Worker(
        client,
        task_queue=DRS_TASK_QUEUE,
        activities=[service.process_drs_payload],
    )
    print("Starting DRS service worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 