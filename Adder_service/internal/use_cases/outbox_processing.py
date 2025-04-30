from internal.adapters.rabbitmq_publisher import RabbitMQPublisher
from internal.adapters.outbox_repository import OutBoxRepository
from internal.entities.outbox_message import Outbox
from internal.utils.logger import setup_logger
import threading,time
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
logger = setup_logger('outbox.log')
class OutBoxProcessor:
    def __init__(self,repository:OutBoxRepository,publisher:RabbitMQPublisher,interval:float,clustersize:int):
        self.repository = repository
        self.publisher = publisher
        self.interval = interval
        self._stop_event = threading.Event()
        self.clustersize = clustersize
    
    
    def process_messages(self):
        logger.info("Fetching pending messages from outbox")
        outboxes = self.repository.GetPendingMessages(self.clustersize)
        if not outboxes:
            logger.info("There are no outbox messages to be processed")
            return

        def handle_message(ob):
            try:
                self.publisher.publish_message("sums", ob.value)
                self.repository.MarkAsProcessed(ob.id)
            except Exception as e:
                logger.error(f"Error processing message ID {ob.id}: {e}")

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(handle_message, ob) for ob in outboxes]
            for future in as_completed(futures):
                future.result()

    
    
