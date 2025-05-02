package com.NumDrift.Sink_service.services;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.rabbitmq.client.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeoutException;

public class Consumer {
    private static final Logger logger = LoggerFactory.getLogger(Consumer.class);
    private Connection connection;
    private Channel channel;
    private final BlockingQueue<Integer> numberQueue = new LinkedBlockingQueue<>();
    private final ObjectMapper objectMapper = new ObjectMapper();
    private static final String QUEUE_NAME = "sums";

    public void start() throws IOException, TimeoutException {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            
            // Get RabbitMQ host from environment variable or use default
            String rabbitHost = System.getenv("SPRING_RABBITMQ_HOST");
            if (rabbitHost == null || rabbitHost.isEmpty()) {
                rabbitHost = "localhost";
            }
            logger.info("Connecting to RabbitMQ at: {}", rabbitHost);
            
            factory.setHost(rabbitHost);
            factory.setConnectionTimeout(5000); // 5 second timeout
            
            connection = factory.newConnection();
            channel = connection.createChannel();
            channel.queueDeclare(QUEUE_NAME, true, false, false, null);

            DeliverCallback deliverCallback = (consumerTag, delivery) -> {
                String message = new String(delivery.getBody(), StandardCharsets.UTF_8);
                try {
                    logger.info("Received message: {}", message);
                    JsonNode jsonNode = objectMapper.readTree(message);
                    int number = jsonNode.get("result").asInt();
                    numberQueue.put(number);
                } catch (Exception e) {
                    logger.error("Failed to process message: {}", message, e);
                }
            };

            channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> {});
            logger.info("Started consuming from queue: {}", QUEUE_NAME);
        } catch (Exception e) {
            logger.error("Failed to connect to RabbitMQ: {}", e.getMessage());
            throw e; // Rethrow to let the application handle it
        }
    }

    public int getNextNumber() throws InterruptedException {
        return numberQueue.take();
    }

    public void close() throws IOException, TimeoutException {
        if (channel != null && channel.isOpen()) {
            channel.close();
        }
        if (connection != null && connection.isOpen()) {
            connection.close();
        }
    }
}