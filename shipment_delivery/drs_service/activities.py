from temporalio import activity
from shipment_delivery.shared.models import ShipmentOrder, OrderStatus
from typing import Dict, Any

class DRSService:
    @activity.defn(name="DRSService.process_drs_payload")
    async def process_drs_payload(self, order_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Convert dictionary to ShipmentOrder
        order = ShipmentOrder.from_dict(order_dict)
        
        order.status = OrderStatus.PUSH_TO_DRS_PAYLOAD
        activity.heartbeat("DRS payload processed")
        
        # Convert back to dictionary
        return order.to_dict() 