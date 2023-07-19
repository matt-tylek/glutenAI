import os
import csv
import spacy
import re
from nltk.tokenize import RegexpTokenizer
from PIL import Image
import pytesseract

# List of ingredients that contain gluten
gluten_ingredients = ['wheat', 'rye', 'barley', 'malt', 'brewer’s yeast', 'oats', 'breaded', 'flour', 'fried']

# Load a spacy model for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")

# Create a cache to store the results of the image conversion
cache = {}

def convert_image_to_text(image_path):
    # Check if the image file is in the cache
    if image_path not in cache:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        cache[image_path] = text
    return cache[image_path]

def is_gluten_free(menu_item):
    # Convert menu_item to lowercase
    menu_item = menu_item.lower()
    # Check each gluten ingredient in the menu_item
    for ingredient in gluten_ingredients:
        # If a gluten ingredient is found, it's not gluten-free
        if ingredient in menu_item:
            return False
    # If no gluten ingredient is found, it's gluten-free
    return True

def text_processing(text):
    # Tokenize the text and join again to remove unwanted characters
    tokenizer = RegexpTokenizer(r'\w+|\s+')
    tokens = tokenizer.tokenize(text)
    # Only keep the words
    words = [token for token in tokens if token.isalpha()]
    cleaned_text = " ".join(words)
    return cleaned_text

def identify_gluten_free_items(image_path):
    # Convert image to text
    text = convert_image_to_string(image_path)
    # Process the text
    cleaned_text = text_processing(text)
    # Perform Named Entity Recognition
    doc = nlp(cleaned_text)
    # Filter named entities that are gluten-free
    gluten_free_items = [ent.text for ent in doc.ents if is_gluten_free(ent.text)]
    return gluten_free_items

# Get all image files in the directory
image_files = [f for f in os.listdir('menus') if f.endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif'))]

with open('gluten_free_items.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Item", "Gluten-Free"])  # Add a Gluten-Free column

    # Process each image file
    for image_file in image_files:
        text = convert_image_to_text(os.path.join('menus', image_file))
        cleaned_text = text_processing(text)
        doc = nlp(cleaned_text)

        # Write the results to the CSV file
        for ent in doc.ents:
            item = ent.text
            gluten_free = is_gluten_free(item)
            writer.writerow([item, int(gluten_free)])  # Write the item and whether it's gluten-free
            
# everything else stays the same ...

# We will store the gluten-free items in a list instead of writing them to a CSV file
gluten_free_items = []

# Process each image file
for image_file in image_files:
    text = convert_image_to_text(os.path.join('menus', image_file))
    cleaned_text = text_processing(text)
    doc = nlp(cleaned_text)

    # Add the items to the list if they're gluten-free
    for ent in doc.ents:
        item = ent.text
        if is_gluten_free(item):
            gluten_free_items.append(item)


