FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY internal/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install psycopg2 and pika explicitly
RUN pip install --no-cache-dir psycopg2-binary pika python-dotenv protobuf grpcio-tools

# Copy the rest of the application
COPY . .

# Update server.py to listen on all interfaces instead of just localhost
RUN sed 's/server.add_insecure_port(.localhost:50051.)/server.add_insecure_port("0.0.0.0:50051")/' server/server.py > server/server_tmp.py \
    && mv server/server_tmp.py server/server.py

# Expose the gRPC port
EXPOSE 50051

# Set the Python path for module imports
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Create a non-root user to run the service
RUN useradd -m appuser
USER appuser

# Run the server
CMD ["python", "server/server.py"] 