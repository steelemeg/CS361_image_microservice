# Using https://www.cloudamqp.com/docs/python.html as a guide

# Pulls requests out of the req_google_images queue, processes them, and sends an appropriate response
# to the res_google_images queue.

import urllib.parse
import pika, os, json

# Import the actual client code and instantiate.
from getGoogleImages import GoogleImages
image_fetcher = GoogleImages()

# Connect to the Cloud AMQP queue using an environment variable.
url = os.getenv('CLOUDAMQP_URL')
parameters = pika.URLParameters(url)
connect = pika.BlockingConnection(parameters)
# Connect to the incoming requests queue.
channel = connect.channel()
channel.queue_declare(queue='req_google_images')

# For each request in the queue, parse it and hand off to the GoogleImages client service.
def process_request(channel, method, properties, req_body):
    print('received message ', str(req_body))
    json_request = {}
    json_response = {'success': True}
    num_images = 10
    image_parameters = ''
    try:
        json_request = json.loads(req_body)
    except ValueError as e:
        json_response =  {'success': False, 'error_message': 'Request body did not contain not valid JSON'}
    else:
        # Parse the request and prepare the search terms. image_parameters is required, num_images is optional.
        if 'image_parameters' not in json_request:
            json_response = {'success': False, 'error_message': 'Missing image_parameters. This is a required field'}

        else:
            if 'num_images' in json_request:
                num_images = json_request['num_images']
            image_parameters = json_request['image_parameters']
            results = image_fetcher.image_query(image_parameters, num_images)
            json_response['images'] = results
            channel.basic_publish(routing_key='res_google_images',
                                  exchange='',
                                  properties=pika.BasicProperties(correlation_id= properties.correlation_id),
                                  body=json.dumps(json_response))

channel.basic_consume(queue='req_google_images', on_message_callback=process_request, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()