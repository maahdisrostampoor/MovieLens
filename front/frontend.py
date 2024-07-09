from flask import Flask, render_template, request, jsonify
import boto3
import os
import requests

# AWS S3 configuration
S3_BUCKET = 'movielens-brocode'  # replace with your S3 bucket name
S3_REGION = 'us-east-1'  # replace with your AWS region

# Initialize Flask application
app = Flask(__name__)

# Configure AWS credentials
s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                  region_name=S3_REGION)

# Function to upload file to S3
def upload_to_s3(file, bucket_name):
    try:
        s3.upload_fileobj(file, bucket_name, file.filename)
        return True
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        return False

# Route for home page with file upload form
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was submitted
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return 'No selected file' 

        # Upload file to S3
        if upload_to_s3(file, S3_BUCKET):
            # Get S3 object URL
            object_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file.filename}"

            # Call API Gateway with S3 object URL
            api_gateway_url = 'https://04ixgz1gx5.execute-api.eu-west-1.amazonaws.com/dev/'  # replace with your API Gateway endpoint URL
            payload = {'image_url': object_url}
            print(payload)

            # Example of sending the URI to API Gateway (you need to implement this part)
            # You can use requests library or any other HTTP client for this purpose
            # For demonstration, we just print the payload
           # print(f"Sending payload to API Gateway: {payload}")
            try:
                # Call the API Gateway
                headers = {'Content-Type': 'application/json'}
                response = requests.post(api_gateway_url, json=payload, headers=headers)
                response_data = response.json()

                return jsonify({
                    'image_url': object_url,
                    'api_gateway_response': response_data
                }), 200
            except Exception as e:
                return jsonify({'error': f"Error calling API Gateway: {str(e)}"}), 500
        else:
            return jsonify({'error': 'Error uploading file to S3'}), 500

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
