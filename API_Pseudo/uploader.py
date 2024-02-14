## Secure File Uploader/Ingester ##

def fileUpload(file, api_key):
    if authenticate(api_key) == "success":
        # Authenticating user
        if identifyFileType(file) == "success":
            # File type is valid
            print("File upload success")
            return "success"
        else:
            # File type is invalid
            print("File upload fail")
            return "failed" 

def authenticate(api_key):
    if api_key == "match":
        # API key valid 
        return "success"
    # API key invalid
    return "failed"

def login(username, password, api_key):
    if username == "match" and password == "match" and authenticate(api_key) == "success":
        # User successfully logs in
        print("Login successful")
        return "success"
    # User fails to log in
    print("Login failed")
    return "failed"

def identifyFileType(file):
    if fileType == "valid":
        # Returns file type and success if file type is valid
        return "success", fileType
    # File type is invalid
    return "failed"
