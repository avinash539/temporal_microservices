from datetime import timedelta
from typing import Dict, Optional
from dataclasses import dataclass
from temporalio import workflow
from temporalio.exceptions import ApplicationError
from enum import Enum
from dataclasses import asdict

class ShipmentStatus(str, Enum):
    CREATED = "CREATED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    EXCEPTION = "EXCEPTION"

@dataclass
class StatusUpdateRequest:
    status: str  # Change to str to handle serialization better
    location: str
    timestamp: str
    notes: Optional[str] = None

    def __post_init__(self):
        # Handle different types of status input
        if isinstance(self.status, list):
            status_value = self.status[0] if self.status else "CREATED"
        elif isinstance(self.status, ShipmentStatus):
            status_value = self.status.value
        elif isinstance(self.status, str):
            status_value = self.status
        else:
            status_value = "CREATED"
        
        # Validate that it's a valid status
        if status_value not in [status.value for status in ShipmentStatus]:
            raise ValueError(f"Invalid status value: {status_value}")
        
        self.status = status_value  # Store as string

    def to_dict(self):
        return {
            "status": self.status,  # Already a string
            "location": self.location,
            "timestamp": self.timestamp,
            "notes": self.notes
        }

@dataclass
class StatusUpdateResponse:
    success: bool
    message: str
    updated_status: str  # Changed to str instead of ShipmentStatus

@workflow.defn
class ShipmentTrackingWorkflow:
    def __init__(self) -> None:
        self._current_status = ShipmentStatus.CREATED.value
        self._status_history: Dict[str, Dict] = {}
        self._completed = False  # Add completion flag
        
    @workflow.run
    async def run(self, shipment_id: str) -> None:
        self._shipment_id = shipment_id
        # Wait until the workflow is marked as completed
        await workflow.wait_condition(lambda: self._completed)
    
    @workflow.update
    async def update_status(self, update_request: StatusUpdateRequest) -> StatusUpdateResponse:
        # Convert string status to enum for validation
        try:
            new_status = ShipmentStatus(update_request.status)
        except ValueError as e:
            raise ApplicationError(f"Invalid status value: {update_request.status}")

        # Validate the status transition
        if not self._is_valid_transition(new_status):
            raise ApplicationError(
                f"Invalid status transition from {self._current_status} to {new_status.value}"
            )
        
        # Update the status
        previous_status = self._current_status
        self._current_status = new_status.value
        self._status_history[update_request.timestamp] = update_request.to_dict()
        
        # Mark workflow as completed if status is DELIVERED
        if new_status == ShipmentStatus.DELIVERED:
            self._completed = True
        
        workflow.logger.info(
            f"Status updated from {previous_status} to {self._current_status}"
        )
        
        return StatusUpdateResponse(
            success=True,
            message=f"Successfully updated status to {self._current_status}",
            updated_status=self._current_status
        )
    
    @workflow.query
    def get_current_status(self) -> str:
        return self._current_status
    
    @workflow.query
    def get_status_history(self) -> Dict[str, Dict]:
        return self._status_history
    
    def _is_valid_transition(self, new_status: ShipmentStatus) -> bool:
        current_status = ShipmentStatus(self._current_status)  # Convert string back to enum
        # Define valid status transitions
        valid_transitions = {
            ShipmentStatus.CREATED: [ShipmentStatus.PICKED_UP, ShipmentStatus.EXCEPTION],
            ShipmentStatus.PICKED_UP: [ShipmentStatus.IN_TRANSIT, ShipmentStatus.EXCEPTION],
            ShipmentStatus.IN_TRANSIT: [ShipmentStatus.OUT_FOR_DELIVERY, ShipmentStatus.EXCEPTION],
            ShipmentStatus.OUT_FOR_DELIVERY: [ShipmentStatus.DELIVERED, ShipmentStatus.EXCEPTION],
            ShipmentStatus.DELIVERED: [ShipmentStatus.EXCEPTION],
            ShipmentStatus.EXCEPTION: [ShipmentStatus.IN_TRANSIT, ShipmentStatus.OUT_FOR_DELIVERY]
        }
        
        return new_status in valid_transitions.get(current_status, []) 