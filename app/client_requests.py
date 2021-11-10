# Using template from https://www.cloudamqp.com/docs/python.html
# Sample client interaction code

import pika, os, json, uuid
custom_queue = 'google_images_AutoDelete'
class ImageRequests(object):

    def __init__(self):

        # Configure connection
        self.url = os.environ.get('CLOUDAMQP_URL')
        self.parameters = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(self.parameters)

        self.channel = self.connection.channel()

        # Results queue can be any value at the user's discretion. This is where the client should
        # listen for image responses, and where the image server will publish responses.
        result = self.channel.queue_declare(queue=custom_queue, exclusive=False, auto_delete=True)
        self.callback_queue = result.method.queue

        # Start listening to the callback queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='google_images_requests',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


google_image_client = ImageRequests()

# Send a test message
message = {'image_parameters': ["mars rover", "xkcd"], "num_images": '3'}
response = google_image_client.call(json.dumps(message))
print("Printing response sent to client from server:")
print(json.loads(response))
