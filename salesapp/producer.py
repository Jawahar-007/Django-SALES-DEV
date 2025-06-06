import pika
import json

params = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')

connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish_order(message: dict):
    # channel.basic_publish(exchange='', routing_key='admin', body = 'Hello Admin, this is a message from the sales app!')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )

if __name__ == "__main__":
    publish_order()
    print("Message sent to order queue")
    connection.close()