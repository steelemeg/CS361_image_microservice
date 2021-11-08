# Pushes responses back to the req_google_images queue
# Using https://www.cloudamqp.com/docs/python.html as a guide
import pika, os, ssl

# Connect to the cloud server
url = os.getenv('CLOUDAMQP_URL')
parameters = pika.URLParameters(url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# Connect to the outgoing/responses queue.
channel.queue_declare(queue='res_google_images')
channel.basic_publish(exchange='', routing_key='req_google_images', \
                      body='{"image_parameters": ["search phrase jaguar", "second test"], "num_images": 2}')
                      #body='i am not json mwaha')
# pull metatags - # - "og:image"