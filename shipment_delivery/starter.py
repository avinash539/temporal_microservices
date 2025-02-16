import asyncio
import uuid
from temporalio.client import Client
from shared.constants import TASK_QUEUE_NAME
from shared.workflow import ShipmentDeliveryWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    
    # Create a unique order ID
    order_id = str(uuid.uuid4())
    
    print(f"Starting shipment delivery workflow for order {order_id}")
    
    result = await client.execute_workflow(
        ShipmentDeliveryWorkflow.run,
        order_id,
        id=f"shipment-delivery-{order_id}",
        task_queue=TASK_QUEUE_NAME,
    )
    
    print(f"Workflow completed. Final order status: {result.status}")
    print(f"Tracking ID: {result.tracking_id}")

if __name__ == "__main__":
    asyncio.run(main()) 