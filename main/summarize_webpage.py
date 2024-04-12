import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import requests
from bs4 import BeautifulSoup
import re

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

def fetch_text_from_webpage(url):
    """
    Fetches text content from a webpage.

    Parameters:
    url (string): URL of the webpage

    Returns:
    text (string): Text content of the webpage
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')  # Assuming paragraphs are contained in 'p' tags
    text = ' '.join([p.text.strip() for p in paragraphs])
    return text

def summarize_webpage(url, sentences_count=4):
    """
    Summarizes a webpage using the LSA algorithm.

    Parameters:
    url (string): URL to webpage
    sentences_count (int): Number of sentences to include in the summary

    Returns:
    summary (string): Summary of the webpage
    """
    try:
        # Fetch text content from the webpage
        text = fetch_text_from_webpage(url)

        # Initialize tokenizer
        tokenizer = AutoTokenizer.from_pretrained('t5-base')                        
        model = AutoModelForSeq2SeqLM.from_pretrained('t5-base', return_dict=True)

        # Tokenize
        inputs = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=512, truncation=True)

        # Create summary
        summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2) 
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        # Capitalize summary
        summary = capitalize_sentences(summary)
        return summary, True
    except Exception as e:
        print(f"Error occurred during summarization: {e}")
        return None, False
