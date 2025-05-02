# NumDrift - Real-time Data Processing System

[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-supported-brightgreen)](https://docs.docker.com/compose/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Java](https://img.shields.io/badge/Java-21-orange)](https://www.java.com/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.4-green)](https://spring.io/projects/spring-boot)
[![gRPC](https://img.shields.io/badge/gRPC-enabled-blue)](https://grpc.io/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12-orange)](https://www.rabbitmq.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)

## Project Overview

NumDrift is a distributed, fault-tolerant, microservices-based system designed for real-time numerical data processing. It consists of two primary microservices that work in concert to provide a reliable and scalable solution for processing and storing numerical data.

The system leverages modern architectural patterns including:
- **Microservices Architecture**: Modular, independently deployable services
- **Event-Driven Design**: Using RabbitMQ for asynchronous messaging
- **Transactional Outbox Pattern**: Ensuring reliable message publishing
- **Containerization**: Docker-based deployment for consistency and portability

## System Architecture

![Architecture Diagram](screenshots/PDtlRkE%20-%20Imgur.png)

### Core Components

#### 1. Adder Service (Python)
A high-performance gRPC service built with Python that:
- Receives numerical inputs via gRPC API
- Processes mathematical operations on the data
- Implements the transactional outbox pattern for reliable messaging
- Publishes processed results to RabbitMQ
- Uses PostgreSQL for data persistence and transactional outbox

**Key Technologies:**
- Python 3.11
- gRPC for high-performance API
- PostgreSQL for data storage
- Pika for RabbitMQ integration

#### 2. Sink Service (Java Spring Boot)
A robust consumer service built with Java Spring Boot that:
- Subscribes to the RabbitMQ queue
- Consumes and processes messages from the Adder Service
- Provides RESTful API endpoints for data access
- Persists processed data for later retrieval

**Key Technologies:**
- Java 21
- Spring Boot 3.4
- Spring AMQP for RabbitMQ integration
- RESTful API design

#### 3. Supporting Infrastructure
- **RabbitMQ**: Message broker for asynchronous communication
- **PostgreSQL**: Relational database for data persistence
- **Docker & Docker Compose**: Containerization for consistent deployment

## Data Flow

1. Client sends numerical data to Adder Service via gRPC
2. Adder Service processes the data and stores it in PostgreSQL
3. Using the outbox pattern, Adder Service publishes results to RabbitMQ
4. Sink Service consumes messages from RabbitMQ queue
5. Sink Service processes and stores the data for access via its REST API

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2+
- 4GB+ RAM available for containers
- Network access for container communication

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/NumDrift.git
cd NumDrift
```

### 2. Launch the System

```bash
docker-compose up -d
```

This command will:
- Build all service containers
- Initialize PostgreSQL database
- Start RabbitMQ message broker
- Launch both Adder and Sink services
- Configure networking between all components

### 3. Monitor the System

```bash
docker-compose logs -f
```

## Service Access Points

| Service | Access Point | Description |
|---------|--------------|-------------|
| Adder Service | gRPC: localhost:50051 | Send numerical data for processing |
| Sink Service | HTTP: http://localhost:8080 | REST API for accessing processed data |
| RabbitMQ Admin | http://localhost:15672 | Management UI (user: guest, pass: guest) |
| PostgreSQL | localhost:5432 | Database access (user: revoo, pass: Refaat2004) |

## Advanced Usage

### Scaling Services

```bash
docker-compose up -d --scale sink-service=3
```

### Manual Database Setup

If PostgreSQL initialization fails:

```bash
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE outbox_db OWNER revoo;"
```

## Troubleshooting

### Common Issues

1. **Database Connection Failures**
   - Ensure PostgreSQL container is running: `docker-compose ps postgres`
   - Check logs: `docker-compose logs postgres`
   - Verify database credentials in environment variables

2. **RabbitMQ Connectivity Issues**
   - Ensure RabbitMQ is healthy: `docker-compose logs rabbitmq`
   - Check if both services are connected to the same network

3. **Service Startup Failures**
   - Review service logs: `docker-compose logs [service-name]`
   - Verify all dependencies are healthy before service startup

## Development Workflow

### Making Changes to Adder Service

1. Modify Python code in `Adder_service/`
2. Rebuild and restart: `docker-compose up -d --build adder-service`

### Making Changes to Sink Service

1. Modify Java code in `Sink_service/`
2. Rebuild with: `docker-compose up -d --build sink-service`

## Project Structure

```
NumDrift/
├── Adder_service/          # Python gRPC service
│   ├── Dockerfile          # Container definition
│   ├── internal/           # Business logic
│   │   ├── adapters/       # External systems integration
│   │   ├── entities/       # Domain objects
│   │   ├── frameworks/     # Framework code
│   │   └── use_cases/      # Application logic
│   └── server/             # Server initialization
├── Sink_service/           # Java Spring Boot service
│   ├── Dockerfile          # Container definition
│   ├── pom.xml             # Maven dependencies
│   └── src/                # Java source code
├── docker-compose.yml      # Container orchestration
└── README.md               # This file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- gRPC for high-performance API capabilities
- Spring Boot for robust Java application framework
- RabbitMQ team for reliable message broker
- PostgreSQL for powerful open-source database
- Docker for containerization technology
