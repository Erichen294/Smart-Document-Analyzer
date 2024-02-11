## Secure File Uploader/Ingester and Text NLP Analysis ##

def fileUpload(file, api_key):
    if authenticate(api_key) == "success":
        if file == "success":
            print("File upload success")
            return "success"
        else:
            print("File upload fail")
            return "Failed" 

def authenticate(api_key):
    if api_key == "match":
        return "success"
    return "failed"

def textAnalysis(text):
    # Tokening strings
    tokens = tokenize(text)

    # Checking frequency
    frequency = countFreq(tokens)

    # Analysis (key terms, frequeny terms)
    analysis = analyze(tokens)

    # Summarize
    summary = summarize(tokens)

    return analysis, summary