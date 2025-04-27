import pika

class RabbitMQPublisher:
    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='sums')

    def publish(self, message):
        self.channel.basic_publish(exchange='', routing_key='sums', body=str(message))

    def close(self):
        self.connection.close()