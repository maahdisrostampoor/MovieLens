from serpapi import GoogleSearch
import requests
import json
from openai import OpenAI
import os

params = {
    "engine": "google_reverse_image",
    "image_url": "" ,
    "api_key": ""
}

search = GoogleSearch(params)
results = search.get_dict()
movie_title_list = []
with open("output.json", "w") as file:
    json.dump(results, file)

if "image_results" in results:
    for result in results["image_results"]:
        source = result.get("source")
        if source in ["IMDb", "Wikipedia","Aeron Systems","Screen Rant"]:
            highlighted_words = result.get("snippet_highlighted_words")
            for item in highlighted_words:
                if item[0] == item[0].upper():
                    movie_title_list.append(item) 
            break


## Open AI 
client = OpenAI(
    api_key = "",
)

# Create the prompt to send to OpenAI
prompt = f"Extract only the name of the movie from these links: {json.dumps(results)}"

# Request movie names from OpenAI API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

movie_name_ai = response.choices[0].message.content

# Print results for debugging
print(f"Movie Title List: {movie_title_list}")
print(f"Movie Name AI: {movie_name_ai}")

# Final movie name extraction
final_movie_name = ""
for movie in movie_title_list:
    if movie == movie_name_ai:
        final_movie_name = movie
        print("Match found")
        break

if not final_movie_name:
    final_movie_name = movie_name_ai


base_url = "http://www.omdbapi.com/"

api_key = ""
# print(set(movie_title_list))
# Title of the movie 
print(movie_name_ai)
params = {
    "apikey": api_key,
    "t": movie_name_ai
}
# Send a GET request to the OMDb API
response = requests.get(base_url, params=params)

# Parse the JSON response
data = response.json()

# Print the movie information
print(data)


