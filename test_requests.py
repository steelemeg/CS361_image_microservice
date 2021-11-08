# Generate test messages
import pika, os

# Connect to the cloud server
url = os.getenv('CLOUDAMQP_URL')
parameters = pika.URLParameters(url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# Connect to the outgoing/responses queue.
channel.exchange_declare(exchange='google_images', exchange_type='direct')
# Bind the queue to the exchange using the routing key
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='google_images', queue=queue_name, routing_key='Megan')
channel.basic_publish(exchange='google_images', routing_key='Megan', \
                      body='{"image_parameters": ["mars rover", "xkcd"], "num_images": 2}')
                      #body='i am not json mwaha')

def testRequest(channel, method, properties, req_body):
    print(req_body)
# Testing
#channel.basic_consume(queue=queue_name, on_message_callback=testRequest, auto_ack=True)
#channel.start_consuming()