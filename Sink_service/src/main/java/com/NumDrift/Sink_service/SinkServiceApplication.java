package com.NumDrift.Sink_service;

import com.NumDrift.Sink_service.services.Consumer;
import com.NumDrift.Sink_service.services.UpdateNumber;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Bean;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

@SpringBootApplication
public class SinkServiceApplication {
	private static final Logger logger = LoggerFactory.getLogger(SinkServiceApplication.class);
	private Consumer consumer;
	private final UpdateNumber updateNumber;
	private Thread connectorThread;
	private volatile boolean running = true;

	public SinkServiceApplication() throws IOException {
		this.updateNumber = new UpdateNumber();
	}

	public static void main(String[] args) {
		ConfigurableApplicationContext context = SpringApplication.run(SinkServiceApplication.class, args);
		SinkServiceApplication app = context.getBean(SinkServiceApplication.class);
		// Give Spring a moment to initialize the consumer bean
		app.startConnector();
		
		Runtime.getRuntime().addShutdownHook(new Thread(() -> {
			try {
				app.shutdown();
			} catch (Exception e) {
				logger.error("Error during shutdown", e);
			}
		}));
	}

	@Bean
	public Consumer consumer() throws IOException, TimeoutException {
		consumer = new Consumer();
		consumer.start();
		return consumer;
	}

	public void startConnector() {
		connectorThread = new Thread(() -> {
			while (running) {
				try {
					int number = consumer.getNextNumber();
					updateNumber.updateNumber(number);
					
					System.out.println("Number processed: " + number);
				} catch (InterruptedException e) {
					if (running) {
						System.err.println("Error getting next number: " + e.getMessage());
					}
				} catch (IOException e) {
					System.err.println("Error updating number: " + e.getMessage());
				}
			}
		});
		
		connectorThread.setDaemon(true);
		connectorThread.start();
		System.out.println("Connector thread started");
	}

	public void shutdown() throws IOException, TimeoutException {
		running = false;
		if (connectorThread != null) {
			connectorThread.interrupt();
		}
		if (consumer != null) {
			consumer.close();
		}
		System.out.println("Application shutting down");
	}
}
