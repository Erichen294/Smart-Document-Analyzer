import pymongo
from bson.objectid import ObjectId
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
from collections import Counter
import queue
import threading
import time

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["documentanalysis"]
documents_collection = db["documents"]

# Initialize the summarization queue
summarization_queue = queue.Queue()

# Lock to ensure thread safety when accessing the queue
queue_lock = threading.Lock()

def summarize_worker():
    while True:
        if not summarization_queue.empty():
            # Pop the summarization task from the queue
            with queue_lock:
                document_id, username = summarization_queue.get()
            
            # Perform summarization
            document = documents_collection.find_one({"_id": ObjectId(document_id), "username": username})
            if document:
                file_contents = document.get("file_contents", "")
                summary, return_val, keywords = summarize_document(file_contents)
                if return_val:
                    # Update the document with the summary and keywords
                    documents_collection.update_one(
                        {"_id": ObjectId(document_id)},
                        {"$set": {"summary": summary, "keywords": keywords}}
                    )
                else:
                    print(f"Failed to summarize document with ID: {document_id}")
            else:
                print(f"Document with ID {document_id} not found.")
        else:
            # Sleep briefly before checking the queue again
            time.sleep(0.1)

# Start summarization worker thread
summarization_thread = threading.Thread(target=summarize_worker)
summarization_thread.daemon = True
summarization_thread.start()

def extract_keywords(text):
    """
    Extracts keywords from the text.

    Parameters:
    text (string): The input text

    Returns:
    keywords (list): List of extracted keywords
    """
    # Define regex pattern for tokenization
    pattern = r"\b\w+\b"

    # Tokenize the text
    words = re.findall(pattern, text.lower())

    # Filter out common words (stopwords)
    stopwords = set(["the", "and", "or", "in", "on", "at", "to", "a", "an", "is", "are", 
                     "was", "were", "for", "of", "with", "by", "as", "this", "that", "these", 
                     "those", "it", "its", "they", "them", "he", "she", "his", "her", "their", 
                     "we", "our", "us", "you", "your", "i", "my", "me", "mine", "from", "areas",
                     "which"])
    filtered_words = [word for word in words if word not in stopwords]

    # Calculate word frequencies
    word_freq = Counter(filtered_words)

    # Get the most common keywords
    keywords = [word for word, freq in word_freq.most_common(5)] 

    return keywords

def capitalize_sentences(summary):
    """
    Capitalizes the first letter of each sentence in the summary.

    Parameters:
    summary (string): The summary text

    Returns:
    capitalized_summary (string): The summary with capitalized sentences
    """
    # Split the summary into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', summary)

    # Capitalize the first letter of each sentence
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]

    # Join the sentences back into a summary
    capitalized_summary = ' '.join(capitalized_sentences)

    return capitalized_summary

def summarize_document(file_name, username):
    """
    Summarizes a document from the database using the LSA algorithm.

    Parameters:
    file_name (string): The name of the document file
    username (string): The username of the current user

    Returns:
    summary (string): Summary of the document
    return_val (bool): True if summarization is successful, False otherwise
    """
    # Find the document by file name and associated username in the MongoDB collection
    document = documents_collection.find_one({"filename": file_name, "username": username})

    if not document or username == None:
        return "Document not found", False
    
    # Get the document contents
    document_contents = document.get("file_contents", "")

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained('t5-base')                        
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")

    # Tokenize
    inputs = tokenizer.encode("summarize: " + document_contents, return_tensors='pt', max_length=512, truncation=True)

    # Create summary
    summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2) 
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Capitalize summary
    summary = capitalize_sentences(summary)

    # Find keywords
    keywords = extract_keywords(document_contents)

    return summary, True, keywords
