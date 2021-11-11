# Uses parameters from Rabbit messages to submit a request to Google Custom Search api.
# Processes response and prepares a return message.
import os, urllib.parse, requests

base_url = 'https://customsearch.googleapis.com/customsearch/v1?'
# Get the api key
api_key = ''
if os.path.isfile('secrets.py'):
    import secrets
    api_key = secrets.GOOGLE_CSKEY
else:
    api_key = os.environ.get('GOOGLE_CSKEY')

# Define the custom search url and ID; use the Google API Python client to manage the connection.
base_url = 'https://customsearch.googleapis.com/customsearch/v1?key='

class GoogleImages():
    def __init__(self):
        self.engine_id = 'd5ead32b6cf2d3fc4'

    def google_request(self, query, num_images):
        request_url = f"{base_url}{api_key}&cx={self.engine_id}&q={query}&num={num_images}&enableImageSearch=True&defaultToImageSearch=True&disableWebSearch=True&searchType=Image"
        response = requests.get(request_url).json()
        if 'items' in response:
            return response['items']
        else:
            return ['Error', response]

    def image_query(self, image_parameters, num_images):
        query_list = []
        results = []

        for parameter in image_parameters:
            # If the search term includes a space, it's a phrase and needs to be wrapped in quotes.
            if ' ' in parameter:
                parameter = '"' + parameter + '"'
            parameter = urllib.parse.quote_plus(parameter)
            query_list.append(parameter)

        # Now build a query string with the formatted parameters.
        query = '+'.join(query_list)
        images_results = self.google_request(query, num_images)
        if images_results[0] != 'Error':
            for image in images_results:
                results.append(image['link'])
        else:
            results = images_results

        return results

