import pymongo
import bcrypt

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["documentanalysis"]  # Choose or create a database

users_collection = db["users"]
documents_collection = db["documents"]

 # Function to register a new user
def register_user(username, password):
    # Check if the username is taken
    if users_collection.find_one({"username": username}):
        return False
    # Hashing password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Insert the new user into the database
    user = {
        "username": username,
        "password": hashed_password.decode('utf-8'),  # Convert bytes to string for storage,
    }
    result = users_collection.insert_one(user)
    return True

# Function to authenticate a user
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return True
    else:
        return False
    
# Function to submit a document
def submit_document(user_id, title, content):
    document = {
        "user_id": user_id,
        "title": title,
        "content": content,
    }
    result = documents_collection.insert_one(document)
    return True