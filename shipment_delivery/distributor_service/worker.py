import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shared.constants import DISTRIBUTOR_TASK_QUEUE
from .activities import DistributorService

async def main() -> None:
    client: Client = await Client.connect("localhost:7233", namespace="default")
    
    # Run the worker
    service = DistributorService()
    worker: Worker = Worker(
        client,
        task_queue=DISTRIBUTOR_TASK_QUEUE,
        activities=[
            service.process_distribution,
            service.initiate_rto
        ],
    )
    print("Starting distributor service worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 