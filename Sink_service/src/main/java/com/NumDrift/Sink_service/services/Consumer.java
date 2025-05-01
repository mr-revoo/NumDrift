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
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        connection = factory.newConnection();
        channel = connection.createChannel();
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);

        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String message = new String(delivery.getBody(), StandardCharsets.UTF_8);
            try {
                JsonNode jsonNode = objectMapper.readTree(message);
                int number = jsonNode.get("result").asInt();
                numberQueue.put(number);
            } catch (Exception e) {
                logger.error("Failed to process message: " + message, e);
            }
        };

        channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> {});
    }

    public int getNextNumber() throws InterruptedException {
        return numberQueue.take();
    }

    public void close() throws IOException, TimeoutException {
        if (channel != null) {
            channel.close();
        }
        if (connection != null) {
            connection.close();
        }
    }
}