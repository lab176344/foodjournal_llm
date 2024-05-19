import spacy


def n_gram_nouns_adjectives(text, n=5):
    # Load the spacy model
    nlp = spacy.load('en_core_web_sm')
    # Parse the text
    doc = nlp(text)
    # Extract the nouns and adjectives
    nouns = [token.text for token in doc if token.pos_ in ('NOUN')]
    adjectives = [token.text for token in doc if token.pos_ in ('ADJ')]

    return nouns, adjectives
