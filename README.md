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
Requests should be published to the 'google_images_requests' queue. For example, when publishing a request, use:
```
routing_key='google_images_requests'
```

Responses will be sent to the unique callback queue of the client's choice, as specified by the routing key. (Full test request code is available in client.requests.py.)
For example, 
```
result = self.channel.queue_declare(queue='google_images_Megan', exclusive=False)
self.callback_queue = result.method.queue
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
 
 
   
