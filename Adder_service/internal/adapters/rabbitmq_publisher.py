import pika
from internal.entities.outbox_message import OutboxMessage

class RabbitMQPublisher:
    queuename:str
    def __init__(self,queuename:str, host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue= queuename)

    def publish(self,message:OutboxMessage):
        self.channel.basic_publish(exchange='', routing_key=self.queuename, body=str(message))

    def close(self):
        self.connection.close()