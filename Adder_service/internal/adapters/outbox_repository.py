from internal.adapters.database_initalizer import InitDB
from internal.entities.outbox_message import Outbox
from internal.utils.logger import setup_logger 
import uuid
logger = setup_logger('outbox.log') 
class OutBoxRepository:
    mess:Outbox
    def __init__(self,db:InitDB):
       self.db = db
       
    def store(self,value:int):
        query = "INSERT INTO outbox (id, value, status) VALUES (%s, %s, %s)"
        try:
            with self.db.get_connection() as conn:
                with conn.get_cursor() as cursor:
                    cursor.execute(query,(self.mess.id,self.mess.payload,self.mess.status)) 
                    logger.info("1 Row Inserted into Table")
        except Exception as e:
            logger.info(f"Insertion Query Failed : {e}")
            
            
    def GetPendingMessages(self,limit):
        messages = []
        query = "SELECT id, sent_at, created_at, value FROM outbox WHERE sent_at IS NULL LIMIT %s"
        with self.db.cursor() as cursor:
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
        for row in rows:
            message = Outbox(
                id=row[0],
                sent_at=row[1],
                created_at=row[2],
                payload=row[3]
            )
            messages.append(message)
        return messages
    
    
    def MarkAsProcessed(self,ID:uuid.uuid4):
        query = "UPDATE outbox SET sent_at = %s where id = %s"
        with self.db.get_cursor as cursor:
            cursor.execute(query,(self.mess.sent_at,ID))
            logger.info(f"Row {ID} has been Marked as processed")