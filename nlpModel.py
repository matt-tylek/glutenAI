import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from collections import defaultdict

from gluten import gluten_free_items

# Load in the data from JSON file
data = pd.read_json('./restaurant.json')

# Here's where you put your list of gluten-free foods
gluten_free_foods = gluten_free_items

# Load the SpaCy model
nlp = spacy.blank('en')

# Create the PhraseMatcher object. The tokenizer is the first argument. 
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

# Create a list of tokens for each item in the menu
food_tokens_list = [nlp(item) for item in gluten_free_foods]

# Add the item patterns to the matcher. 
matcher.add("MENU", None, *food_tokens_list)

# item_ratings is a dictionary of lists. If a key doesn't exist in item_ratings,
# the key is added with an empty list as the value.
item_ratings = defaultdict(list)

for idx, review in data.iterrows():
    doc = nlp(review.text)
    matches = matcher(doc)
    found_items = set([str(doc[match[1]:match[2]]).lower() for match in matches])
    for item in found_items:
        item_ratings[item].append(review.stars)

# Calculate the mean ratings for each menu item as a dictionary
mean_ratings = {item: sum(ratings)/len(ratings) for item, ratings in item_ratings.items()}

# Print out the average ratings for each gluten-free item
for item, rating in mean_ratings.items():
    print(f"Item: {item}, Average rating: {rating}")
