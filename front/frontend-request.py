import requests

# URL of your API Gateway endpoint
url = 'https://nnjbk1ac5a.execute-api.us-east-1.amazonaws.com/Prod/'

# Path to the image file
image_file_path = '/home/maahdis/Pictures/matrix.jpeg'

# Prepare the image file to be sent
files = {
    'image': ('image.jpg', open(image_file_path, 'rb'), 'image/jpeg')
}

try:
    # Send POST request with multipart form data to API Gateway
    response = requests.post(url, files=files)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print('Image uploaded successfully.')
        print('Response:', response.json())  # Assuming the response is JSON
    else:
        print('Failed to upload image. Status code:', response.json())

except requests.exceptions.RequestException as e:
    print('Error uploading image:', e)
