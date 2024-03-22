import requests
import pymongo
import bcrypt
import database
import summarizer

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["documentanalysis"] 

users_collection = db["users"]
documents_collection = db["documents"]

username = ""
def register():
    global username
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Call the register_user function from database.py
    success = database.register_user(username, password)
    if success:
        print("User registered successfully.")
    else:
        print("Username already exists. Please choose another username.")

def login():
    global username
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    response = requests.post(f"http://127.0.0.1:5000/api/login", json={'username': username, 'password': password})
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        print(response.json())
        return None

def upload_document(access_token):
    document_path = input("Enter path to document: ")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    files = {'document': open(document_path, 'rb')}
    
    response = requests.post(f"http://127.0.0.1:5001/api/upload", headers=headers, files=files)
    print(response.json())

def main():
    global username
    while True:
        print("\nOptions:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            access_token = login()
            if access_token:
                while True:
                    print("\nOptions:")
                    print("1. Upload Document")
                    print("2. Analyze document")
                    print("3. Logout")
                    inner_choice = input("Enter your choice: ")

                    if inner_choice == '1':
                        upload_document(access_token)
                    elif inner_choice == '2':
                        file_name = input("Enter file name: ")
                        summary, return_val = summarizer.summarize_document(file_name, username)
                        if return_val:
                            print("Summary: ", summary)
                        else:
                            print(summary)
                    elif inner_choice == '3':
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
