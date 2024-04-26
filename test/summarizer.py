import re
from collections import Counter

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