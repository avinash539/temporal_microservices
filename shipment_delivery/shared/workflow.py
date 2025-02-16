from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from shared.models import ShipmentOrder
from shared.constants import (
    PRS_TASK_QUEUE,
    DISTRIBUTOR_TASK_QUEUE,
    HUBOPS_TASK_QUEUE,
    NETWORK_PARTNERS_TASK_QUEUE,
    DRS_TASK_QUEUE,
    TRACKING_TASK_QUEUE
)
from typing import Dict, Any
from .base_workflow import RetryableWorkflow

@workflow.defn
class ShipmentDeliveryWorkflow(RetryableWorkflow):
    def __init__(self):
        super().__init__()
        self._order: ShipmentOrder = None

    @workflow.run
    async def run(self, order_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Convert dictionary to ShipmentOrder
        self._order = ShipmentOrder.from_dict(order_dict)
        
        # Create PRS
        result = await self.execute_with_retry_and_pause(
            "PRSService.create_prs",
            "PRS Service",
            self._order.to_dict(),
            PRS_TASK_QUEUE
        )
        self._order = ShipmentOrder.from_dict(result)

        # Process distribution
        result = await self.execute_with_retry_and_pause(
            "DistributorService.process_distribution",
            "Distributor Service",
            self._order.to_dict(),
            DISTRIBUTOR_TASK_QUEUE
        )
        self._order = ShipmentOrder.from_dict(result)

        # Process hub operations
        result = await self.execute_with_retry_and_pause(
            "HubOpsService.process_hub_operations",
            "HubOps Service",
            self._order.to_dict(),
            HUBOPS_TASK_QUEUE
        )
        self._order = ShipmentOrder.from_dict(result)

        # Assign delivery partner
        result = await self.execute_with_retry_and_pause(
            "NetworkPartnersService.assign_delivery_partner",
            "Network Partners Service",
            self._order.to_dict(),
            NETWORK_PARTNERS_TASK_QUEUE
        )
        self._order = ShipmentOrder.from_dict(result)

        # Process DRS payload
        result = await self.execute_with_retry_and_pause(
            "DRSService.process_drs_payload",
            "DRS Service",
            self._order.to_dict(),
            DRS_TASK_QUEUE
        )
        self._order = ShipmentOrder.from_dict(result)

        # Update tracking
        result = await self.execute_with_retry_and_pause(
            "TrackingService.update_tracking",
            "Tracking Service",
            self._order.to_dict(),
            TRACKING_TASK_QUEUE
        )
        self._order = ShipmentOrder.from_dict(result)

        return self._order.to_dict() 