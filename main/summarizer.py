import pymongo
from bson.objectid import ObjectId
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["documentanalysis"]
documents_collection = db["documents"]

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
    return summary, True
