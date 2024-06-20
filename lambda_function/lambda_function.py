import logging
from typing import Dict
from reverse_image_search import GoogleReverseImageSearch

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | [%(levelname)s]: %(message)s',
    datefmt='%m-%d-%Y / %I:%M:%S %p'
)

# Instantiate the GoogleReverseImageSearch class
reverse_image_search = GoogleReverseImageSearch()

def lambda_handler(event, context):
    # Extract query parameters from the event
    query_params = event.get('queryStringParameters', {})
    query = query_params.get('query')
    image_url = query_params.get('image_url')

    # Perform the reverse image search
    try:
        max_results = 10  # Default max results
        response = reverse_image_search.response(query, image_url, max_results)
        return {
            'statusCode': 200,
            'body': str(response),
            'headers': {
                'Content-Type': 'text/plain'
            }
        }
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': "Internal Server Error",
            'headers': {
                'Content-Type': 'text/plain'
            }
        }

