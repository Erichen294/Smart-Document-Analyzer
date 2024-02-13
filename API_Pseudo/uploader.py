## Secure File Uploader/Ingester ##

def fileUpload(file, api_key):
    if authenticate(api_key) == "success":
        if identifyFileType(file) == "success":
            print("File upload success")
            return "success"
        else:
            print("File upload fail")
            return "failed" 

def authenticate(api_key):
    if api_key == "match":
        return "success"
    return "failed"

def login(username, password, api_key):
    if username == "match" and password == "match" and authenticate(api_key) == "success":
        print("Login successful")
        return "success"
    print("Login failed")
    return "failed"

def identifyFileType(file):
    if fileType == "valid":
        return "success", fileType
    return "failed"