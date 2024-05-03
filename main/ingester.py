from googlesearch import search

def search_articles(keywords, num_results=2):
    """
    Perform Google searches using keywords and return URLs of relevant articles.

    Parameters:
    keywords (list): List of keywords to search for.
    num_results (int): Number of search results to retrieve for each keyword. Default is 2.

    Returns:
    urls (dict): Dictionary containing URLs of relevant articles for each keyword.
    """
    urls = []
    num = 0
    keyword = keywords[0]
    for keyword in keywords:
        for j in search(keyword, tld="co.in", num=10, stop=10, pause=2):
            if num < 2:
                urls.append(j)
                num += 1
            else:
                num = 0
                break
    return urls
