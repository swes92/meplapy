# meplapy/text_extractor.py

import pdfplumber
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
import csv

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + ' '
    return text.strip()

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def extract_text_from_csv(file_path):
    text = ''
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            text += ' '.join(row) + ' '  # Concatenate rows with spaces
    return text.strip()

def extract_locations(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Perform part-of-speech tagging
    pos_tags = pos_tag(tokens)
    # Perform named entity recognition
    named_entities = ne_chunk(pos_tags)

    # Extract location entities
    locations = []
    for chunk in named_entities:
        if hasattr(chunk, 'label') and chunk.label() == 'GPE':  # GPE stands for Geo-Political Entity
            locations.append(' '.join(c[0] for c in chunk))

    return locations
