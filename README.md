# CS361_image_microservice
 
### Retrieves images from Google using RabbitMQ and custom search.

<!-- TOC -->
   - [Installation and Environment](#installation)
   - [Creating a test Rabbit request](#test-request)
   - [JSON parameters](#json)
   - [Consuming and responding](#response)
<!-- /TOC -->

## Installation

Relies on a hosted instance of CloudAMQP/RabbitMQ. The service details are controlled using the CLOUDAMQP_URL environment variable. 
Relies on pika and requests.
  
Connects to a Google custom search engine; the API key is stored in the GOOGLE_CSKEY environment variable.


## Test Request
Note that requests and responses use RabbitMQ exchanges and routing keys to manage messaging.
Requests should be sent to the google_images exchange with a routing key corresponding to the team member's name. For example: 
```
  # Connect to the cloud server
  url = os.getenv('CLOUDAMQP_URL')
  parameters = pika.URLParameters(url)
  connection = pika.BlockingConnection(parameters)
  channel = connection.channel()
  
  # Connect to the Google images queue.
  channel.exchange_declare(exchange='google_images', exchange_type='direct')
  
  # Bind the queue to the exchange using the routing key
  result = channel.queue_declare(queue='', exclusive=True)
  queue_name = result.method.queue
  channel.queue_bind(exchange='google_images', queue=queue_name, routing_key='Megan')
  channel.basic_publish(exchange='google_images', routing_key='Megan', \
                        body='{"image_parameters": ["mars rover", "xkcd"], "num_images": 2}')
```

## JSON

```json
{
  "image_parameters": ["xkcd", "mars rover"]
  "num_images":       3
 }
 ```
 - **image_parameters** [List] - Required. Any number of image search terms. These may include phrases. 
 - **num_images** [Number]  - Optional. A number specifying how many image links the requestor wants to receive. Default is currently 10.
     
## Response
**Successful Request**
```json
{
"success":     true,
"image_urls": ["https://imgs.xkcd.com/comics/spirit.png", 
               "https://www.explainxkcd.com/wiki/images/2/27/opportunity_rover.png", 
               "https://imgs.xkcd.com/comics/opportunity.png"]
}
```
**Failure**
```json
{
  "success":        false, 
  "error_message": "Request body did not contain not valid JSON"
}
```
 - **success** [Boolean] - Whether the service was able to successfully generate a response from the request.
 - **error_message** [String] - A description of the issue.
 
 
   
