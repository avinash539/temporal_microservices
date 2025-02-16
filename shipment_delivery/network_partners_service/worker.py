import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shipment_delivery.shared.constants import NETWORK_PARTNERS_TASK_QUEUE
from .activities import NetworkPartnersService

async def main() -> None:
    client = await Client.connect("localhost:7233", namespace="default")
    
    # Run the worker
    service = NetworkPartnersService()
    worker = Worker(
        client,
        task_queue=NETWORK_PARTNERS_TASK_QUEUE,
        activities=[service.assign_delivery_partner],
    )
    print("Starting network partners service worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 