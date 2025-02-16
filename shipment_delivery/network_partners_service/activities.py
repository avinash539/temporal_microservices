from temporalio import activity
from shipment_delivery.shared.models import ShipmentOrder
from typing import Dict, Any

class NetworkPartnersService:
    @activity.defn(name="NetworkPartnersService.assign_delivery_partner")
    async def assign_delivery_partner(self, order_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Convert dictionary to ShipmentOrder
        order = ShipmentOrder.from_dict(order_dict)
        
        # Assign to 3PL (Shipyaari)
        activity.heartbeat("Delivery partner assigned")
        
        # Convert back to dictionary
        return order.to_dict() 