from temporalio import activity
from shared.models import ShipmentOrder, OrderStatus
from typing import Dict, Any

class DistributorService:
    @activity.defn(name="DistributorService.process_distribution")
    async def process_distribution(self, order_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Convert dictionary to ShipmentOrder
        order = ShipmentOrder.from_dict(order_dict)
        
        # Process distribution logic
        order.status = OrderStatus.IN_SCAN_FM
        activity.heartbeat("Distribution processed")
        
        # Convert back to dictionary
        return order.to_dict()

    @activity.defn(name="DistributorService.initiate_rto")
    async def initiate_rto(self, order_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Convert dictionary to ShipmentOrder
        order = ShipmentOrder.from_dict(order_dict)
        
        order.status = OrderStatus.RTO_INITIATED
        activity.heartbeat("RTO initiated")
        
        # Convert back to dictionary
        return order.to_dict() 