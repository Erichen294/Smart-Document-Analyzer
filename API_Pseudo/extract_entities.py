import spacy
import summarize_webpage

# Load English language model
nlp = spacy.load("en_core_web_sm")

def is_valid_entity(entity_text):
    """
    Checks if an entity's text contains only valid alphanumeric characters.

    Parameters:
    entity_text (str): The text of the entity.

    Returns:
    bool: True if the entity's text contains only valid alphanumeric characters, False otherwise.
    """
    return all(char.isalnum() or char.isspace() for char in entity_text)

def extract_entities(text):
    """
    Extracts names, locations, and institutions from the text.

    Parameters:
    text (str): The input text.

    Returns:
    entities (dict): A dictionary containing lists of names, locations, and institutions.
    """
    # Process the text
    doc = nlp(text)

    # Initialize sets to store entities
    names = set()
    locations = set()
    institutions = set()

    # Iterate over named entities
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            if is_valid_entity(entity.text):
                names.add(entity.text)
        elif entity.label_ == "GPE" or entity.label_ == "LOC":
            if is_valid_entity(entity.text):
                locations.add(entity.text)
        elif entity.label_ == "ORG":
            if is_valid_entity(entity.text):
                institutions.add(entity.text)

    # Create dictionary of entities
    entities = {
        "names": names,
        "locations": locations,
        "institutions": institutions,
    }

    return entities

text = summarize_webpage.fetch_text_from_webpage("https://en.wikipedia.org/wiki/Riemann_hypothesis")
entities = extract_entities(text)
print(entities)
