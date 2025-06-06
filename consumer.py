import pika

params = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')
def callback(ch, method, properties, body):
    print(f"Received in Admin")
    print(f"Message: {body.decode()}")

def main():
    params = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='order_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='order_queue', on_message_callback=callback)
    print('Started consuming')
    channel.start_consuming()

if __name__ == "__main__":
    main()
    print("Consumer is running")
    connection.close()
