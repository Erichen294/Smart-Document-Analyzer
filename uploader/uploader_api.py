import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, decode_token
import pymongo

app = Flask(__name__)

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["documentanalysis"]
documents_collection = db["documents"]

# Configure allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Check if the uploaded file has a permitted extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to retrieve username from access token
def get_username_from_token(access_token):
    try:
        decoded_token = decode_token(access_token)
        print("Decoded Token:", decoded_token)
        username = decoded_token['sub']
        return username
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        return None
    
# File upload endpoint
@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Check if the 'Authorization' header is present in the request
    if 'Authorization' not in request.headers:
        return jsonify({'error': 'Missing Authorization header'}), 401

    # Extract the token from the 'Authorization' header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]
    print("Access Token:", access_token)

    # Check if the POST request has the file part
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['document']

    # If user does not select file, browser also submits an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file has a permitted extension
    if file and allowed_file(file.filename):
        # Secure filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        
        # Get the username associated with the access token (You need to implement this)
        username = get_username_from_token(access_token)
        
        # Read the file contents as a string
        file_contents = file.read().decode('utf-8')

        # Insert the document into the MongoDB collection
        document = {
            "username": username,
            "filename": filename,
            "file_contents": file_contents
        }
        documents_collection.insert_one(document)
        
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
