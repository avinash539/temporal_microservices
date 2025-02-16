import asyncio
from datetime import datetime
from temporalio.client import Client
from temporalio.exceptions import ApplicationError
from shared.update_workflow import (
    ShipmentTrackingWorkflow,
    ShipmentStatus,
    StatusUpdateRequest
)
from shared.constants import TRACKING_UPDATE_TASK_QUEUE

async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")
    
    # Generate a unique shipment ID
    shipment_id = "SHIP-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    
    try:
        # Start the workflow
        handle = await client.start_workflow(
            ShipmentTrackingWorkflow.run,
            shipment_id,
            id=shipment_id,
            task_queue=TRACKING_UPDATE_TASK_QUEUE,
        )
        
        print(f"Started workflow with ID: {shipment_id}")
        
        # Example of synchronous status updates
        try:
            # Update 1: PICKED_UP
            result = await handle.execute_update(
                ShipmentTrackingWorkflow.update_status,
                StatusUpdateRequest(
                    status="PICKED_UP",
                    location="Warehouse A",
                    timestamp=datetime.now().isoformat(),
                    notes="Package picked up from origin"
                )
            )
            print(f"Update 1 result: {result.message}")
            
            # # Update 2: Try an invalid transition (should fail)
            # try:
            #     result = await handle.execute_update(
            #         ShipmentTrackingWorkflow.update_status,
            #         StatusUpdateRequest(
            #             status="DELIVERED",
            #             location="Invalid Location",
            #             timestamp=datetime.now().isoformat(),
            #         )
            #     )
            # except ApplicationError as e:
            #     print(f"Expected error for invalid transition: {str(e)}")
            # except Exception as e:
            #     print(f"Unexpected error during invalid transition test: {str(e)}")
            
            # Update 2: IN_TRANSIT
            result = await handle.execute_update(
                ShipmentTrackingWorkflow.update_status,
                StatusUpdateRequest(
                    status="IN_TRANSIT",
                    location="Transit Hub B",
                    timestamp=datetime.now().isoformat(),
                    notes="Package in transit to destination"
                )
            )
            print(f"Update 2 result: {result.message}")

            # Update 3: OUT_FOR_DELIVERY
            result = await handle.execute_update(
                ShipmentTrackingWorkflow.update_status,
                StatusUpdateRequest(
                    status="OUT_FOR_DELIVERY",
                    location="Local Delivery Hub",
                    timestamp=datetime.now().isoformat(),
                    notes="Package out for final delivery"
                )
            )
            print(f"Update 3 result: {result.message}")

            # Update 4: DELIVERED
            result = await handle.execute_update(
                ShipmentTrackingWorkflow.update_status,
                StatusUpdateRequest(
                    status="DELIVERED",
                    location="Customer Address",
                    timestamp=datetime.now().isoformat(),
                    notes="Package successfully delivered to customer"
                )
            )
            print(f"Update 4 result: {result.message}")
            
            # Query current status
            current_status = await handle.query(ShipmentTrackingWorkflow.get_current_status)
            print(f"\nFinal status: {current_status}")
            
            # Query status history
            history = await handle.query(ShipmentTrackingWorkflow.get_status_history)
            print("\nComplete Status History:")
            for timestamp, update in sorted(history.items()):
                print(f"{timestamp}: {update['status']} at {update['location']}")
                if update.get('notes'):
                    print(f"  Notes: {update['notes']}")
                
        except ApplicationError as e:
            print(f"Workflow application error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error during updates: {str(e)}")
            raise  # Re-raise to see the full stack trace
            
    except Exception as e:
        print(f"Error starting workflow: {str(e)}")
        raise  # Re-raise to see the full stack trace

if __name__ == "__main__":
    asyncio.run(main()) 