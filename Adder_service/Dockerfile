FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY internal/requirements.txt ./requirements.txt

# Install dependencies with specific compatible versions
RUN pip install --no-cache-dir grpcio grpcio-tools protobuf
RUN pip install --no-cache-dir psycopg2-binary pika python-dotenv

# Copy the rest of the application
COPY . .

# Update server.py to listen on all interfaces and use rabbitmq host
RUN sed -i 's/server.add_insecure_port(.localhost:50051.)/server.add_insecure_port("0.0.0.0:50051")/' server/server.py && \
    sed -i 's/RabbitMQPublisher(queuename="sums")/RabbitMQPublisher(queuename="sums", host="rabbitmq")/' server/server.py && \
    sed -i 's/Server started on localhost:50051/Server started on 0.0.0.0:50051/' server/server.py

# Expose the gRPC port
EXPOSE 50051

# Set the Python path for module imports
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Run the server
CMD ["python", "server/server.py"] 