import pika
import json
import os
import django
from decouple import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communication_service.settings')  # Replace with your project name
django.setup()

from .helper import perform_operation


class RpcServer:
    def __init__(self):
        connection = pika.BlockingConnection(pika.URLParameters(config('RABBITMQ_URL')))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='communication_queue')
        self.channel.basic_consume(queue='communication_queue', on_message_callback=self.on_request, auto_ack=True)\
            
            
    def on_request(self, ch, method, properties, body):
        value = json.loads(body)
        response = perform_operation(value)
         
        
        self.channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=str(response)
        )
        
    def start(self):
        self.channel.start_consuming()
        
        
if __name__ == '__main__':
    server = RpcServer()
    server.start()