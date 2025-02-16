from temporalio import activity
import uuid
from shared.models import ShipmentOrder, OrderStatus
from typing import Dict, Any

class PRSService:
    @activity.defn(name="PRSService.create_prs")
    async def create_prs(self, order_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Convert dictionary to ShipmentOrder
        order = ShipmentOrder.from_dict(order_dict)
        
        # Create PRS (Pickup Request Service) entry
        order.prs_id = str(uuid.uuid4())
        order.status = OrderStatus.PICKED_UP
        activity.heartbeat("PRS created")
        
        # Convert back to dictionary
        return order.to_dict()