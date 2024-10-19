# meplapy/ner.py

import nltk
from nltk import pos_tag, word_tokenize, ne_chunk

# Make sure to download the required NLTK datasets the first time you run the code
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker_tab')


def extract_locations(text):
    """
    Extract location names (GPE - Geopolitical Entities) from text and include 3-word context before and after each location.
    """
    # Tokenize and perform POS tagging
    tokenized_doc = word_tokenize(text)
    tagged_sentences = pos_tag(tokenized_doc)

    # Named Entity Recognition
    ne_tree = ne_chunk(tagged_sentences)

    # Extract GPEs (Geopolitical Entities) and context
    locations_with_context = []
    for i, subtree in enumerate(ne_tree):
        if hasattr(subtree, 'label') and subtree.label() == 'GPE':
            entity_name = ' '.join([leaf[0] for leaf in subtree.leaves()])

            # Get context: 3 words before and 3 words after
            start_idx = max(0, i - 5)
            end_idx = min(len(tokenized_doc), i + 5)
            context = ' '.join(tokenized_doc[start_idx:end_idx])

            locations_with_context.append((entity_name, context))

    return locations_with_context