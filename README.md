# NumDrift - Containerized Services

This repository contains a microservices-based system with two main components:
1. **Adder Service**: A Python gRPC service that processes data and publishes messages to RabbitMQ
2. **Sink Service**: A Java Spring Boot application that consumes messages from RabbitMQ

The system has been containerized using Docker and Docker Compose for easy deployment.

## Architecture

- **Adder Service**: Python-based gRPC service that adds numbers and publishes the results to a RabbitMQ queue
- **Sink Service**: Java Spring Boot application that consumes messages from RabbitMQ
- **RabbitMQ**: Message broker for communication between services
- **PostgreSQL**: Database for the Adder Service to store outbox messages

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/NumDrift.git
   cd NumDrift
   ```

2. Start the services:
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

3. Monitor the logs:
   ```bash
   docker-compose logs -f
   ```

## Service Endpoints

- **Adder Service**: gRPC service running on port 50051
- **Sink Service**: HTTP service running on port 8080
- **RabbitMQ Management UI**: http://localhost:15672 (username: guest, password: guest)
- **PostgreSQL**: Available on localhost:5432

## Stopping the Services

```bash
docker-compose down
```

To remove all data (including volumes):
```bash
docker-compose down -v
```

## Development

### Making Changes to the Adder Service

1. Modify the Python code in the `Adder_service` directory
2. Rebuild and restart the service:
   ```bash
   docker-compose up -d --build adder-service
   ```

### Making Changes to the Sink Service

1. Modify the Java code in the `Sink_service` directory
2. Rebuild and restart the service:
   ```bash
   docker-compose up -d --build sink-service
   ```
