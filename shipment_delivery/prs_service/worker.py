import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shipment_delivery.shared.constants import PRS_TASK_QUEUE
from shipment_delivery.prs_service.activities import PRSService

async def main() -> None:
    client: Client = await Client.connect("localhost:7233", namespace="default")
    
    # Run the worker
    service = PRSService()
    worker: Worker = Worker(
        client,
        task_queue=PRS_TASK_QUEUE,
        activities=[service.create_prs],
    )
    print("Starting PRS service worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 