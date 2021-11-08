# Uses parameters from Rabbit messages to submit a request to Google Custom Search api.
# Processes response and prepares a return message.
import os, urllib.parse
from googleapiclient.discovery import build

# Get the api key
api_key = os.environ.get('GOOGLE_CSKEY')

# Define the custom search url and ID; use the Google API Python client to manage the connection.
base_url = 'https://customsearch.googleapis.com/customsearch/v1?'
engine_id = 'd5ead32b6cf2d3fc4'
connection = build('customsearch', 'v1', developerKey=api_key)

class GoogleImages():
    def __init__(self):
        self.routing_key = 'res_google_images'

    def image_query(self, image_parameters, num_images):
        query_list = []
        for parameter in image_parameters:
            # If the search term includes a space, it's a phrase and needs to be wrapped in quotes.
            if ' ' in parameter:
                parameter = '"' + parameter + '"'
            parameter = urllib.parse.quote_plus(parameter)
            query_list.append(parameter)
        # Now build a query string with the formatted parameters.
        query = '+'.join(query_list)
        print(query)
        return
