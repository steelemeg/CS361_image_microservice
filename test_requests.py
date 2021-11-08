# Generate test messages
import pika, os

# Connect to the cloud server
url = os.getenv('CLOUDAMQP_URL')
parameters = pika.URLParameters(url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# Connect to the outgoing/responses queue.
channel.queue_declare(queue='res_google_images')
channel.basic_publish(exchange='', routing_key='req_google_images', \
                      body='{"image_parameters": ["mars rover", "xkcd"], "num_images": 2}')
                      #body='i am not json mwaha')
