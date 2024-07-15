import requests
import base64

# URL of your API Gateway endpoint
url = 'https://nnjbk1ac5a.execute-api.us-east-1.amazonaws.com/Prod/'

# Path to the image file
image_file_path = '/home/maahdis/Pictures/godfather.jpg'

# Prepare the image file to be sent
with open(image_file_path, 'rb') as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    print(image_base64)

# Prepare JSON payload
payload = {
    'image_base64': image_base64,
    'filename': 'image.jpg'
}

# Set headers for application/json
headers = {
    'Content-Type': 'application/json'
}


# Send POST request with JSON payload
response = requests.post(url, json=payload, headers=headers)
def rlen(response):
    """
    approximate request size sent to server
    """
    len_of_meth = len(response.request.method)
    len_of_addr = len(response.request.url)
    len_of_head = len('\r\n'.join('{}{}'.format(k, v) for k, v in response.request.headers.items()))
    len_of_body = len(response.request.body if response.request.body else [])

    return len_of_meth + len_of_addr + len_of_head + len_of_body

print(rlen(response))
    # Check if the request was successful (status code 200)
if response.status_code == 200:
    print('Image uploaded successfully.')
    print('Response:', response.json())  # Assuming the response is JSON
else:
    print('Failed to upload image. Status code:', response.json())

