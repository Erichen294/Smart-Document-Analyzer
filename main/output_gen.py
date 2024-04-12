def output_gen(summary, return_val, keywords = None, urls= None):
    if return_val and keywords and urls:
        print("\nSummary: ", summary)
        print("\nKeywords: ", keywords)
        for keyword, article_urls in urls.items():
            print(f"\nArticles for keyword '{keyword}':")
            for url in article_urls:
                print(url)
    elif return_val and summary:
        print("\nSummary: ", summary)
    elif return_val and summary and keywords:
        print("\nSummary: ", summary)
        print("\nKeywords: ", keywords)
    else:
        print("\n", summary)