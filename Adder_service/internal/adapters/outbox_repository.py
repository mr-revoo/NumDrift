from internal.adapters.database_initalizer import InitDB
from internal.entities.outbox_message import Outbox
from internal.utils.logger import setup_logger 
import uuid
from datetime import datetime

logger = setup_logger('outbox.log')

class OutBoxRepository:
    def __init__(self, db:InitDB):
        self.db = db
        self.mess = None
       
    def store(self, value:int):
        query = "INSERT INTO outbox (id, value, status) VALUES (%s, %s, %s)"
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, (self.mess.id, value, self.mess.status))
                logger.info(f"Row with ID {self.mess.id} inserted into outbox table")
        except Exception as e:
            logger.error(f"Insertion Query Failed: {e}")
            
    def GetPendingMessages(self, limit):
        messages = []
        query = "SELECT id, sent_at, created_at, value, status FROM outbox WHERE status = 'NONPROCESSED' LIMIT %s"
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()
                for row in rows:
                    message = Outbox(
                        id=row[0],
                        sent_at=row[1] if row[1] else datetime.now(),
                        created_at=row[2],
                        payload=row[3],
                        status=row[4]
                    )
                    messages.append(message)
                return messages
        except Exception as e:
            logger.error(f"Failed to fetch pending messages: {e}")
            return []
    
    def MarkAsProcessed(self, ID):
        query = "UPDATE outbox SET sent_at = %s, status = %s WHERE id = %s"
        try:
            with self.db.get_cursor() as cursor:
                sent_at = datetime.now()
                cursor.execute(query, (sent_at, "PROCESSED", ID))
                logger.info(f"Row {ID} has been marked as processed")
                return True
        except Exception as e:
            logger.error(f"Failed to mark message {ID} as processed: {e}")
            return False