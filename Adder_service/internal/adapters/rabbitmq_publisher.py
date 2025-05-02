import pika
import json
import time
from internal.entities.outbox_message import Outbox
from internal.utils.logger import setup_logger

logger = setup_logger('rabbitmq.log')

class RabbitMQPublisher:
    def __init__(self, queuename, host='localhost', max_retries=3):
        self.queuename = queuename
        self.host = host
        self.max_retries = max_retries
        self.connection = None
        self.channel = None
        self._connect()
        
    def _connect(self):
        """Establish connection to RabbitMQ with retry logic"""
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                logger.info(f"Connecting to RabbitMQ at {self.host}")
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queuename, durable=True)
                logger.info(f"Successfully connected to RabbitMQ and declared queue {self.queuename}")
                return True
            except Exception as e:
                retry_count += 1
                logger.error(f"Failed to connect to RabbitMQ (attempt {retry_count}/{self.max_retries}): {e}")
                if retry_count >= self.max_retries:
                    logger.error("Max retries reached. Giving up on RabbitMQ connection.")
                    raise
                time.sleep(1)  
        return False

    def _ensure_connection(self):
        """Ensure we have an active connection before publishing"""
        if self.connection is None or self.connection.is_closed:
            return self._connect()
        
        if self.channel is None or self.channel.is_closed:
            try:
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queuename, durable=True)
                return True
            except Exception as e:
                logger.error(f"Failed to create channel: {e}")
                self.connection = None
                return self._connect()
        return True

    def publish(self, message):
        """Original publish method - kept for backwards compatibility"""
        try:
            self._ensure_connection()
            
            if isinstance(message, Outbox):
                payload = message.payload
            else:
                payload = message
            
            self.channel.basic_publish(
                exchange='', 
                routing_key=self.queuename, 
                body=str(payload)
            )
            logger.info(f"Message published to queue {self.queuename}")
            return True
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            self.connection = None  # Force reconnection next time
            raise
        
    def publish_message(self, routing_key, payload):
        """New method that the outbox processor is trying to call"""
        try:
            self._ensure_connection()
            
            message = json.dumps({"result": payload})
            self.channel.basic_publish(
                exchange='', 
                routing_key=routing_key, 
                body=message
            )
            logger.info(f"Message published to queue {routing_key}")
            return True
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            self.connection = None  # Force reconnection next time
            raise

    def close(self):
        """Safely close the connection"""
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
                logger.info("RabbitMQ connection closed")
            except Exception as e:
                logger.error(f"Error closing RabbitMQ connection: {e}")