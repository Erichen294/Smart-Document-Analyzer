import pymongo
from bson.objectid import ObjectId
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
from collections import Counter
import queue
import threading
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize the text
    tokens = text.lower().split()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    conjunctions = [
    "also",
    "and",
    "but",
    "or",
    "nor",
    "for",
    "yet",
    "so",
    "although",
    "because",
    "since",
    "unless",
    "until",
    "while",
    "after",
    "before",
    "if",
    "than",
    "whether",
    "that",
    "as",
    "once",
    "whereas",
    "provided",
    "even",
    "though",
    "while",
    "where",
    "whenever",
    "wherever",
    "however",
    "moreover",
    "nevertheless",
    "therefore",
    "otherwise",
    "hence",
    "accordingly",
    "consequently",
    "thus",
    "similarly",
    "likewise",
    "instead",
    "alternatively",
    "regardless",
    "otherwise",
    "nonetheless",
    "besides",
    "furthermore",
    "on the other hand",
    "in addition",
    "indeed"
    ]
    stop_words.update(conjunctions)
    tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back into text
    cleaned_text = ' '.join(tokens)
    
    # Initialize TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the cleaned text
    tfidf_matrix = vectorizer.fit_transform([cleaned_text])

    # Get the feature names (words) from the vectorizer
    feature_names = vectorizer.get_feature_names()

    # Get the TF-IDF scores for each word
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Create a dictionary to store words and their corresponding TF-IDF scores
    word_tfidf = dict(zip(feature_names, tfidf_scores))

    # Sort the words by their TF-IDF scores in descending order
    sorted_words_tfidf = sorted(word_tfidf.items(), key=lambda x: x[1], reverse=True)

    # Get the top 5 keywords with the highest TF-IDF scores
    top_keywords = [word for word, _ in sorted_words_tfidf[:5]]

    return top_keywords

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

def analyze_tone(text):
    # Initialize VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Analyze sentiment
    sentiment_scores = analyzer.polarity_scores(text)

    # Determine sentiment label
    if sentiment_scores['compound'] >= 0.05:
        return 'This text is positive'
    elif sentiment_scores['compound'] <= -0.05:
        return 'This text is negative'
    else:
        return 'This text is neutral'