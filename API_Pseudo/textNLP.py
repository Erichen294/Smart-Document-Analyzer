## Text NLP Analysis ##

def textAnalysis(text):
    # Tokening strings by paragraph
    tokens = tokenize(text)

    # Checking frequency
    frequency = countFreq(tokens)

    # Analysis (key terms, frequent terms, names, locations, institutions, addresses)
    analysis = analyze(tokens)

    # Summarize
    summary = summarize(tokens)

    # Categorize paragraphs
    positive, neutral, negative = categorize(tokens)

    return analysis, summary, positive, neutral, negative