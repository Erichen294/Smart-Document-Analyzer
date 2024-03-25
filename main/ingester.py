from googlesearch import search

def search_articles(keywords, num_results=2):
    """
    Perform Google searches using keywords and return URLs of relevant articles.

    Parameters:
    keywords (list): List of keywords to search for.
    num_results (int): Number of search results to retrieve for each keyword. Default is .

    Returns:
    urls (dict): Dictionary containing URLs of relevant articles for each keyword.
    """
    urls = {}
    for keyword in keywords:
        urls[keyword] = []
        query = f"{keyword} article"
        for url in search(query, num_results=num_results):
            urls[keyword].append(url)
    return urls
