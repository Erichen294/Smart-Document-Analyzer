from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords

def extract_keywords(text):
    # Tokenize the text
    words = text.lower().split()

    # Filter out stopwords
    stop_words = set(stopwords.words('english'))

    # Calculate TF-IDF scores
    count_vectorizer = CountVectorizer()
    term_counts = count_vectorizer.fit_transform([text])
    tfidf_transformer = TfidfTransformer()
    tfidf_matrix = tfidf_transformer.fit_transform(term_counts)

    # Get the feature names (i.e., words)
    feature_names = count_vectorizer.get_feature_names()

    # Get the TF-IDF scores for the words
    tfidf_scores = tfidf_matrix.toarray().flatten()

    # Combine words with their TF-IDF scores
    word_tfidf_pairs = list(zip(feature_names, tfidf_scores))

    # Sort words by TF-IDF scores in descending order
    sorted_word_tfidf_pairs = sorted(word_tfidf_pairs, key=lambda x: x[1], reverse=True)

    # Get the top 5 keywords
    keywords = [pair[0] for pair in sorted_word_tfidf_pairs[:5]]

    keywords_without_stopwords = [word for word in keywords if word not in stop_words]

    return keywords_without_stopwords