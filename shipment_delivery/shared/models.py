from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

class OrderStatus(Enum):
    ORDER_CREATED = "ORDER_CREATED"
    READY_FOR_DISPATCH = "READY_FOR_DISPATCH"
    PICKED_UP = "PICKED_UP"
    IN_SCAN_FM = "IN_SCAN_FM"
    IN_SCAN_LM = "IN_SCAN_LM"
    RTO_INITIATED = "RTO_INITIATED"
    PUSH_TO_DRS_PAYLOAD = "PUSH_TO_DRS_PAYLOAD"

@dataclass
class ShipmentOrder:
    order_id: str
    customer_id: str
    pickup_address: str
    delivery_address: str
    status: OrderStatus
    created_at: str  # ISO format datetime string
    updated_at: str  # ISO format datetime string
    tracking_id: Optional[str] = None
    prs_id: Optional[str] = None
    hubops_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the order to a dictionary with enum value converted to string."""
        d = asdict(self)
        d['status'] = self.status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ShipmentOrder':
        """Create an order from a dictionary, converting string back to enum."""
        data['status'] = OrderStatus(data['status'])
        return cls(**data) 