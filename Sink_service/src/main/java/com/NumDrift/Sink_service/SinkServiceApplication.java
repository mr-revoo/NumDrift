package com.NumDrift.Sink_service;

import com.NumDrift.Sink_service.services.Consumer;
import com.NumDrift.Sink_service.services.UpdateNumber;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;

import java.io.IOException;

@SpringBootApplication
public class SinkServiceApplication {
	private static final Logger logger = LoggerFactory.getLogger(SinkServiceApplication.class);
	private final UpdateNumber updateNumber;

	@Autowired
	public SinkServiceApplication(UpdateNumber updateNumber) {
		this.updateNumber = updateNumber;
		logger.info("SinkServiceApplication initialized");
	}

	public static void main(String[] args) {
		SpringApplication.run(SinkServiceApplication.class, args);
		logger.info("SinkService application started");
	}

	@Bean
	@Profile("!test") // Skip in test profile
	public CommandLineRunner initRabbitMQ() {
		return args -> {
			logger.info("Attempting to initialize RabbitMQ connection");
			try {
				Consumer consumer = new Consumer();
				consumer.start();
				
				// Start processing in a separate thread
				Thread processor = new Thread(() -> {
					while (!Thread.currentThread().isInterrupted()) {
						try {
							int number = consumer.getNextNumber();
							updateNumber.updateNumber(number);
							logger.info("Processed number: {}", number);
						} catch (InterruptedException e) {
							Thread.currentThread().interrupt();
							logger.info("Processing thread interrupted");
						} catch (Exception e) {
							logger.error("Error processing number", e);
						}
					}
				});
				processor.setDaemon(true);
				processor.start();
				
				logger.info("RabbitMQ connection established and processing started");
			} catch (Exception e) {
				// Just log the error but allow application to continue
				logger.error("Failed to connect to RabbitMQ: {}", e.getMessage());
				logger.info("Application will continue without RabbitMQ connection");
			}
		};
	}
}
