from temporalio import activity
import uuid
from shared.models import ShipmentOrder, OrderStatus
from typing import Dict, Any
from temporalio.exceptions import ApplicationError

class NotRetryableError(ApplicationError):
    """Error that should not be retried"""
    pass

class HubOpsService:
    @activity.defn(name="HubOpsService.process_hub_operations")
    async def process_hub_operations(self, order_dict: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # a = 1/0
            # Convert dictionary to ShipmentOrder
            order = ShipmentOrder.from_dict(order_dict)
            
            # Simulate some processing that might fail
            await self._process_hub_operations(order)
            
            order.hubops_id = str(uuid.uuid4())
            order.status = OrderStatus.IN_SCAN_LM
            activity.heartbeat("Hub operations processed")
            
            # Convert back to dictionary
            return order.to_dict()
        except Exception as e:
            # If it's a critical error that shouldn't be retried, raise NotRetryableError
            if isinstance(e, NotRetryableError):
                raise
            # For other errors, raise as is to allow retry
            raise ApplicationError(f"Hub operations processing failed: {str(e)}")
    
    async def _process_hub_operations(self, order: ShipmentOrder) -> None:
        """Internal method to process hub operations. Can be extended with actual business logic."""
        # Add your actual hub operations processing logic here
        # If there's a critical error, raise NotRetryableError
        # For retryable errors, raise regular exceptions
        pass 