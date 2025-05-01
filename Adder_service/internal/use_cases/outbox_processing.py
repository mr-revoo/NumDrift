from internal.adapters.rabbitmq_publisher import RabbitMQPublisher
from internal.adapters.outbox_repository import OutBoxRepository
from internal.entities.outbox_message import Outbox
from internal.utils.logger import setup_logger
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = setup_logger('outbox.log')

class OutBoxProcessor:
    def __init__(self, repository:OutBoxRepository, publisher:RabbitMQPublisher, interval:float, clustersize:int):
        self.repository = repository
        self.publisher = publisher
        self.interval = interval
        self.clustersize = clustersize
    
    def start(self):
        logger.info("Starting outbox processor")
        try:
            while True:
                self.process_messages()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("Shutting down outbox processor")
            if self.publisher:
                self.publisher.close()
            
    def process_messages(self):
        logger.info("Fetching pending messages from outbox")
        outboxes = self.repository.GetPendingMessages(self.clustersize)
        if not outboxes:
            logger.info("There are no outbox messages to be processed")
            return

        def handle_message(ob):
            retries = 3
            for attempt in range(retries):
                try:
                    self.publisher.publish_message(self.publisher.queuename, ob.payload)
                    self.repository.MarkAsProcessed(ob.id)
                    logger.info(f"Successfully processed and published message ID {ob.id}")
                    return True
                except Exception as e:
                    logger.error(f"Error processing message ID {ob.id} (attempt {attempt+1}/{retries}): {e}")
                    if attempt < retries - 1:
                        # Wait a bit before retrying
                        time.sleep(1)
                    else:
                        # If all retries fail, log and move on
                        logger.error(f"Failed to process message ID {ob.id} after {retries} attempts")
                        return False

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(handle_message, ob) for ob in outboxes]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Unhandled exception in message processing: {e}")

    
    
