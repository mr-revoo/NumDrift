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

WORKDIR /app

# Copy the JAR file from the build stage
COPY --from=build /app/target/*.jar app.jar

# Expose the application port
EXPOSE 8080

# Run the Spring Boot application
ENTRYPOINT ["java", "-jar", "app.jar"] 