import json
import os
import logging
from serpapi import GoogleSearch
from openai import OpenAI
import boto3
import requests
from amazondax import AmazonDaxClient
import base64
from requests_toolbelt.multipart import decoder


# Initialize DAX client
# dax_endpoint = os.getenv('DAX_ENDPOINT')  # DAX endpoint 
# dax = AmazonDaxClient(endpoint_url=dax_endpoint)

# # Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('MovieLens')
ssm_client = boto3.client('ssm')
s3_client = boto3.client('s3')
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

        image_base64 = event.get("image_base64")
        filename = event.get("filename")
        movie_name = event.get("movie_name")
        
        # If image and filename is present in request body
        if image_base64 and filename:
            # Decode the image
            image_data = base64.b64decode(image_base64)

            # Store in S3 bucket
            s3_bucket = os.getenv('S3_BUCKET_NAME')
            s3_region = os.getenv('S3_REGION')
            s3_key = f"{filename}"

            # Store in S3 bucket
            s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=image_data)
            image_url = f"https://{s3_bucket}.s3.{s3_region}.amazonaws.com/{s3_key}"
            if not image_url:
                raise ValueError("image_url is required in the event or as a file")


            # Perform business logic in separate functions
            results = perform_google_image_search(image_url)
            movie_title_list = extract_movie_titles(results)
            movie_name_ai = perform_openai_check(results)
            final_movie_name = get_final_movie_name(movie_title_list, movie_name_ai)
            print(final_movie_name)
        
        # If movie_name is present
        elif movie_name:
            final_movie_name = movie_name
        else:
            raise ValueError("Either image_base64 and filename or movie_name must be provided.")


       # Check cache first
        # movie_detail = get_movie_detail_from_cache(final_movie_name)
        # if not movie_detail:
        #     print("not cache")
        movie_detail = get_movie_detail(final_movie_name)
        store_movie_detail(movie_detail)

        # Related Movie Details
        related_movies = get_related_movies(movie_detail['Genre'].split(', ')[0])
        movie_detail['RelatedMovies'] = related_movies
            
        return format_response(200, movie_detail)
    
    except Exception as e:
        logger.error(f"Error processing the event: {str(e)}")
        return format_response(500, {"error": str(e)})


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
    
    prompt = f"Extract only the name of the movie from these links, give only the name: {json.dumps(results)}"
    
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

#Fetch Related Movies "Genre"
def get_related_movies(genre):

    params = {
        'apikey': OMDB_API_KEY,
        's': genre,  
        'type': 'movie' 
    }

    response = requests.get(movie_database_url, params=params)

    related_movies = []
    
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':

            for movie in data.get('Search', [])[:4]:
                related_movies.append(movie)

    return related_movies


# def get_movie_detail_from_cache(movie_name):
#     print("from cache")
#     try:
#         response = dax.get_item(
#             TableName="MovieLens",
#             Key={'Title': {'S': movie_name}}
#         )
#         return response.get('Item')
#     except Exception as e:
#         logger.error(f"Error getting item from cache: {str(e)}")
#         return None

def format_response(status_code, body):
    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "multiValueHeaders": {},
        "body": json.dumps(body)
    }
    
def store_movie_detail(movie_detail):
    # Define attributes in Dynamodb
    try:
        imdbID = movie_detail.get('imdbID')
        if not imdbID:
            raise ValueError("imdbID is required and must be valid")

        item = {
            'imdbID': {'S': imdbID},
            'Title': {'S': movie_detail.get('Title') or ''},
            'Year': {'S': movie_detail.get('Year') or ''},
            'Rated': {'S': movie_detail.get('Rated') or ''},
            'Released': {'S': movie_detail.get('Released') or ''},
            'Runtime': {'S': movie_detail.get('Runtime') or ''},
            'Genre': {'S': movie_detail.get('Genre') or ''},
            'Director': {'S': movie_detail.get('Director') or ''},
            'Writer': {'S': movie_detail.get('Writer') or ''},
            'Actors': {'S': movie_detail.get('Actors') or ''},
            'Plot': {'S': movie_detail.get('Plot') or ''},
            'Language': {'S': movie_detail.get('Language') or ''},
            'Country': {'S': movie_detail.get('Country') or ''},
            'Awards': {'S': movie_detail.get('Awards') or ''},
            'Poster': {'S': movie_detail.get('Poster') or ''},
            'Metascore': {'S': movie_detail.get('Metascore') or ''},
            'imdbRating': {'S': movie_detail.get('imdbRating') or ''},
            'imdbVotes': {'S': movie_detail.get('imdbVotes') or ''},
            'Type': {'S': movie_detail.get('Type') or ''},
            'DVD': {'S': movie_detail.get('DVD') or ''},
            'BoxOffice': {'S': movie_detail.get('BoxOffice') or ''},
            'Production': {'S': movie_detail.get('Production') or ''},
            'Website': {'S': movie_detail.get('Website') or ''},
            'Response': {'S': movie_detail.get('Response') or ''}
        }
 # Iterate through Ratings sources and add to the item dictionary
        for rating in movie_detail.get('Ratings', []):
            item[rating['Source']] = {'S': rating['Value']}

        # Remove empty attributes
        item = {k: v for k, v in item.items() if v['S']}

        # Store item in DAX
        # dax.put_item(
        #     TableName='MovieLens',
        #     Item=item
        # )

        # Store item in DynamoDB
        dynamodb_item = {k: v['S'] for k, v in item.items()}
        table.put_item(Item=dynamodb_item)

    except Exception as e:
        logger.error(f"Error storing item in cache: {str(e)}")
        raise
