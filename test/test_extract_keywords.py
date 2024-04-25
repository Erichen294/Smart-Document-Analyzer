import pytest
import summarizer

def test_extract_keywords_tokenization():
    text = "This is a sample text. It contains some words."
    keywords = summarizer.extract_keywords(text)
    assert len(keywords) > 0  # Ensure some keywords are extracted

def test_extract_keywords_common_words_filtered():
    text = "The quick brown fox jumps over the lazy dog."
    keywords = summarizer.extract_keywords(text)
    assert "the" not in keywords  # Check if common words are filtered out

def test_extract_keywords_most_common():
    text = "apple banana banana apple cherry cherry cherry"
    keywords = summarizer.extract_keywords(text)
    assert keywords == ["cherry", "banana", "apple"]  or keywords == ["cherry", "apple", "banana"] # Check if most common keywords are extracted

def test_extract_keywords_lowercase():
    text = "This is a Sample Text."
    keywords = summarizer.extract_keywords(text)
    assert "sample" in keywords  # Check if text is lowercased before processing

def test_extract_keywords_empty_text():
    text = ""
    keywords = summarizer.extract_keywords(text)
    assert keywords == []  # Check if empty text returns empty list