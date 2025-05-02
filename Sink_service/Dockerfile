FROM maven:3.9.6-eclipse-temurin-21 as build

WORKDIR /app

# Copy the pom.xml file for dependency resolution
COPY pom.xml .

# Download dependencies (this layer will be cached if pom.xml doesn't change)
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn package -DskipTests

# Use a smaller runtime image
FROM eclipse-temurin:21-jre-jammy

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the wait script
COPY --chmod=755 wait-for-it.sh /usr/local/bin/wait-for-it.sh

# Copy the JAR file from the build stage
COPY --from=build /app/target/*.jar app.jar

# Expose the application port
EXPOSE 8080

# Wait for RabbitMQ to be ready before starting the application
ENTRYPOINT ["sh", "-c", "wait-for-it.sh ${SPRING_RABBITMQ_HOST:-rabbitmq}:5672 --timeout=60 -- java -jar app.jar"] 