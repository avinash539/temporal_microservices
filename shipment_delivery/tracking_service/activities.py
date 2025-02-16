from temporalio import activity
import uuid
from shipment_delivery.shared.models import ShipmentOrder
from typing import Dict, Any

class TrackingService:
    @activity.defn(name="TrackingService.update_tracking")
    async def update_tracking(self, order_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Convert dictionary to ShipmentOrder
        order = ShipmentOrder.from_dict(order_dict)
        
        if not order.tracking_id:
            order.tracking_id = f"TRACK-{str(uuid.uuid4())[:8]}"
        activity.heartbeat(f"Tracking updated: {order.status}")
        
        # Convert back to dictionary
        return order.to_dict() 