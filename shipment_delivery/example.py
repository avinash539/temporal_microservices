import asyncio
from booking_service.service import BookingService

async def main():
    # Create a booking
    booking_service = BookingService()
    order = await booking_service.create_booking(
        pickup_address="123 Pickup St",
        delivery_address="456 Delivery Ave"
    )
    
    print(f"Created order with ID: {order.order_id}")
    print(f"Initial status: {order.status}")

if __name__ == "__main__":
    asyncio.run(main()) 