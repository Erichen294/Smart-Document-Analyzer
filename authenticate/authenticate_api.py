from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pymongo
import bcrypt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'  # Temporary key
jwt = JWTManager(app)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["documentanalysis"]
users_collection = db["users"]

# User login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username exists in the database
    user = users_collection.find_one({"username": username})

    if user:
        # Check if the password matches
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Password matches, generate access token
            access_token = create_access_token(identity=username)
            print("Access Token:", access_token)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'User does not exist'}), 401

# Protected endpoint
@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
