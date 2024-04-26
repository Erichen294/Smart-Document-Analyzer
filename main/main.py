import requests
import pymongo
import bcrypt
import database
import summarizer
import ingester
import output_gen
import summarize_webpage

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
                    print("3. Analyze webpage")
                    print("4. Logout")
                    inner_choice = input("Enter your choice: ")

                    if inner_choice == '1':
                        upload_document(access_token)
                    elif inner_choice == '2':
                        file_name = input("Enter file name: ")
                        summary, return_val, keywords = summarizer.summarize_document(file_name, username)
                        urls = ingester.search_articles(keywords)
                        output_gen.output_gen(summary, return_val, keywords, urls)
                    elif inner_choice == '3':
                        web_url = input("Enter web url: ")
                        webpage_summary, return_val = summarize_webpage.summarize_webpage(web_url)
                        print(webpage_summary)
                        keywords = summarizer.extract_keywords(webpage_summary)
                        print(keywords)
                        # TODO: add better algorithm to find keywords and try to fix google too many url requests error
                        # Update: am using TLK
                        #urls = ingester.search_articles(keywords)
                        #output_gen.output_gen(webpage_summary, return_val, keywords)
                    elif inner_choice == '4':
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
