from datetime import datetime
import uuid
from shared.models import OrderStatus, ShipmentOrder

class BookingService:
    # def __init__(self, order_delivery_service_url: str = "http://localhost:8080"):
    #     self.order_delivery_service_url = order_delivery_service_url

    async def create_booking(self, pickup_address: str, delivery_address: str) -> ShipmentOrder:
        # Create a new order
        current_time = datetime.now().isoformat()
        order = ShipmentOrder(
            order_id=str(uuid.uuid4()),
            customer_id=str(uuid.uuid4()),
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            status=OrderStatus.ORDER_CREATED,
            created_at=current_time,
            updated_at=current_time,
        )

        # Call order delivery service directly
        from order_delivery_service.service import OrderDeliveryService
        order_service = OrderDeliveryService()
        await order_service.initialize()
        await order_service.push_order(order)
        
        return order

    # async def create_booking_http(self, pickup_address: str, delivery_address: str) -> ShipmentOrder:
    #     # This shows how it would work in a real microservices environment
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post(
    #             f"{self.order_delivery_service_url}/orders",
    #             json={
    #                 "pickup_address": pickup_address,
    #                 "delivery_address": delivery_address,
    #             }
    #         ) as response:
    #             response.raise_for_status()
    #             order_data = await response.json()
    #             return ShipmentOrder(**order_data) 