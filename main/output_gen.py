def output_gen(summary, return_val, keywords, urls):
    if return_val:
        print("\nSummary: ", summary)
        print("\nKeywords: ", keywords)
        for keyword, article_urls in urls.items():
            print(f"\nArticles for keyword '{keyword}':")
            for url in article_urls:
                print(url)
    else:
        print("\n", summary)