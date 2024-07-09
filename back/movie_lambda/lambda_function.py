import json
import os
import logging
from serpapi import GoogleSearch
from openai import OpenAI
import boto3
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize clients
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('Movie')
ssm_client = boto3.client('ssm')
movie_database_url = "http://www.omdbapi.com/"


# Get the parameters
def get_parameter(parameter_name):
    response = ssm_client.get_parameter(
        Name=parameter_name,
        WithDecryption=True 
    )
    return response['Parameter']['Value']

# Fetch API keys from Parameter Store
try:
    GOOGLE_API_KEY = get_parameter("GOOGLE_API_KEY")
    OMDB_API_KEY = get_parameter("OMDB_API_KEY")
except Exception as e:
    logger.error(f"Error fetching API keys: {str(e)}")
    raise

# Environment Api key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def lambda_handler(event, context):
    try:
        # Extract the body-json from the event
        body_json = event.get('body-json', {})
        print(body_json)
        image_url = body_json["image_url"]
        if not image_url:
            raise ValueError("image_url is required in the event") 

        # Perform business logic in separate functions
        results = perform_google_image_search(image_url)
        movie_title_list = extract_movie_titles(results)
        movie_name_ai = perform_openai_check(results)
        final_movie_name = get_final_movie_name(movie_title_list, movie_name_ai)

        movie_detail = get_movie_detail(final_movie_name)
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

def perform_google_image_search(image_url):
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": GOOGLE_API_KEY
    }
    
    search = GoogleSearch(params)
    return search.get_dict()

def extract_movie_titles(results):
    movie_title_list = []
    if "image_results" in results:
        for result in results["image_results"]:
            source = result.get("source")
            if source in ["IMDb", "Wikipedia", "Aeron Systems", "Screen Rant"]:
                highlighted_words = result.get("snippet_highlighted_words", [])
                for item in highlighted_words:
                    if item[0] == item[0].upper():
                        movie_title_list.append(item) 
                break
    return movie_title_list

def perform_openai_check(results):

    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"Extract only the name of the movie from these links: {json.dumps(results)}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def get_final_movie_name(movie_title_list, movie_name_ai):
    for movie in movie_title_list:
        if movie == movie_name_ai:
            return movie
    return movie_name_ai


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
