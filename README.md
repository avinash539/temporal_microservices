# Temporal Microservices Examples

This repository consists of temporal-based micro-service examples demonstrating workflow orchestration using Temporal.

## Prerequisites

- Python 3.7 or higher
- Docker and Docker Compose
- Temporal Server

## Setup

1. **Install Python Dependencies**

   ```bash
   pip install temporalio
   ```

2. **Install Project Package**

   ```bash
   cd shipment_delivery
   pip install -e .
   ```

3. **Start Temporal Server Locally**

   Install the Temporal CLI and run the Temporal Server:

   ```bash
   temporal server start-dev --db-filename shipment_db.db
   ```

   you can visit the Temporal Web UI at `http://localhost:8233`

## Project Structure

- `shipment_delivery/` - Contains shipment delivery and tracking workflow examples
  - `update_example.py` - Example demonstrating status updates for a shipment
  - `example.py` - Basic booking and delivery service example
  - `shared/` - Common workflow definitions and utilities
  - `booking_service/` - Booking service implementation
  - `distributor_service/` - Distributor service implementation
  - `drs_service/` - Delivery routing service implementation
  - `hubops_service/` - Hub operations service implementation
  - `network_partners_service/` - Network partners service implementation
  - `order_delivery_service/` - Order delivery service implementation
  - `prs_service/` - Package routing service implementation
  - `tracking_service/` - Shipment tracking service implementation

## Running the Examples

### Required Workers

Before running any examples, you need to start the necessary workers. Each service has its own worker that needs to be running:

1. **Start Core Workers**

   ```bash
   # Terminal 1 - Main workflow worker
   python shipment_delivery/workflow_worker.py

   # Terminal 2 - Update workflow worker
   python shipment_delivery/update_workflow_worker.py
   ```

2. **Start Service Workers** (each in a separate terminal)

   ```bash
   # Terminal 3 - Booking Service
   python shipment_delivery.booking_service.worker.py

   # Terminal 4 - Distributor Service
   python shipment_delivery.distributor_service.worker.py

   # Terminal 5 - DRS Service
   python shipment_delivery.drs_service.worker.py

   # Terminal 6 - HubOps Service
   python shipment_delivery.hubops_service.worker.py

   # Terminal 7 - Network Partners Service
   python shipment_delivery.network_partners_service.worker.py

   # Terminal 8 - PRS Service
   python shipment_delivery.prs_service.worker.py

   # Terminal 9 - Tracking Service
   python shipment_delivery.tracking_service.worker.py
   ```

### Running Example Workflows

Once all workers are running, you can execute the example workflows:

### 1. Shipment Tracking Example

This example demonstrates a workflow for tracking shipment status updates:

1. In a new terminal, run the example:
   ```bash
   python shipment_delivery/update_example.py
   ```

The example will:

- Create a new shipment with a unique ID
- Update the shipment status through various stages (PICKED_UP → IN_TRANSIT → OUT_FOR_DELIVERY → DELIVERED)
- Display the status updates and final history

### 2. Booking Service Example

This example shows a basic booking service workflow:

1. In a new terminal, run the example:
   ```bash
   python shipment_delivery/example.py
   ```

### 3. Complete Shipment Delivery Flow

To test the complete shipment delivery flow with all services:

1. In a new terminal, run:
   ```bash
   python shipment_delivery/starter.py
   ```

This will:

- Create a new booking
- Initiate the delivery workflow
- Coordinate between all services
- Track the shipment status

## Monitoring

1. **Temporal Web UI**

   - Access the Temporal Web UI at `http://localhost:8233`
   - View workflow executions, histories, and worker details

2. **Worker Logs**
   - Each worker outputs logs to its terminal
   - Monitor these logs for debugging and tracking workflow progress

## Troubleshooting

1. **Worker Connection Issues**

   - Ensure Temporal server is running
   - Verify each worker is connected to the correct task queue
   - Check for any error messages in worker terminals

2. **Workflow Execution Problems**
   - Check if all required workers are running
   - Verify task queue names match between workers and workflow code
   - Review workflow execution history in Temporal Web UI
