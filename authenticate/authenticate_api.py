from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'  # Temporary key
jwt = JWTManager(app)

# Sample database of users
users = {
    'me': {
        'password': 'password',
    }
}

# User registration endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'message': 'User already exists'}), 400

    users[username] = {'password': password}
    return jsonify({'message': 'User registered successfully'}), 201

# User login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username not in users or users[username]['password'] != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

# Protected endpoint
@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
