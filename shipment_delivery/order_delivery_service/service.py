from datetime import datetime
import uuid
from temporalio.client import Client
from shared.models import ShipmentOrder, OrderStatus
from shared.constants import WORKFLOW_TASK_QUEUE
from shared.workflow import ShipmentDeliveryWorkflow

class OrderDeliveryService:
    def __init__(self):
        self.temporal_client = None

    async def initialize(self):
        if not self.temporal_client:
            self.temporal_client = await Client.connect("localhost:7233")

    async def push_order(self, order: ShipmentOrder) -> None:
        """Receive order from booking service and start the workflow"""
        # Convert order to dictionary for JSON serialization
        order_dict = order.to_dict()
        
        # Start the workflow
        workflow_id = f"shipment-delivery-{order.order_id}"
        await self.temporal_client.execute_workflow(
            ShipmentDeliveryWorkflow.run,
            order_dict,
            id=workflow_id,
            task_queue=WORKFLOW_TASK_QUEUE,
        )