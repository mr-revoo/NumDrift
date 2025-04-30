from internal.adapters.rabbitmq_publisher import RabbitMQPublisher
from internal.adapters.outbox_repository import OutBoxRepository
from internal.entities.outbox_message import Outbox
from internal.utils.logger import setup_logger
import threading,time
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
        
        if(len(outboxes)== 0):
            logger.info("There is no outbox Messages to be processed")
        
        for outbox in outboxes:
            ob = Outbox()
         # to be completed  
    
    
