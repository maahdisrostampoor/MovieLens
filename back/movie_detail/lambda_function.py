import json
import boto3
import requests
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('Movie')

# Validate environment variables
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
movie_database_url = "http://www.omdbapi.com/"

def lambda_handler(event, context):
    try:
        movie_name = event["movie_name"]  

        movie_detail = get_movie_detail(movie_name)
        store_movie_detail(movie_detail)
    
        return {
            "statusCode": 200,
            "body": json.dumps(movie_detail)
        }
    except Exception as e:
        logger.error(f"Error processing the event: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }



def get_movie_detail(movie_name):
    params = {
        "apikey": OMDB_API_KEY,
        "t": movie_name
    }

    movie_detail = requests.get(movie_database_url, params=params)
    return movie_detail.json()

def store_movie_detail(movie_detail):
    # Define attributes in Dynamodb
    item = {
        'imdbID': movie_detail.get('imdbID'),
        'Title': movie_detail.get('Title'),
        'Year': movie_detail.get('Year'),
        'Rated': movie_detail.get('Rated'),
        'Released': movie_detail.get('Released'),
        'Runtime': movie_detail.get('Runtime'),
        'Genre': movie_detail.get('Genre'),
        'Director': movie_detail.get('Director'),
        'Writer': movie_detail.get('Writer'),
        'Actors': movie_detail.get('Actors'),
        'Plot': movie_detail.get('Plot'),
        'Language': movie_detail.get('Language'),
        'Country': movie_detail.get('Country'),
        'Awards': movie_detail.get('Awards'),
        'Poster': movie_detail.get('Poster'),
        'Metascore': movie_detail.get('Metascore'),
        'imdbRating': movie_detail.get('imdbRating'),
        'imdbVotes': movie_detail.get('imdbVotes'),
        'Type': movie_detail.get('Type'),
        'DVD': movie_detail.get('DVD'),
        'BoxOffice': movie_detail.get('BoxOffice'),
        'Production': movie_detail.get('Production'),
        'Website': movie_detail.get('Website'),
        'Response': movie_detail.get('Response')
    }

    # Iterate through Ratings sources
    for rating in movie_detail.get('Ratings', []):
        item[rating['Source']] = rating['Value']

    # Insert item into the table
    table.put_item(Item=item)
