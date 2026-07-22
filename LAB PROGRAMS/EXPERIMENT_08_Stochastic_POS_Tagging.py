import nltk
from nltk.tag import UnigramTagger
from nltk.tokenize import word_tokenize

# Training data
train_data = [
    [("The", "DT"), ("cat", "NN"), ("sleeps", "VBZ")],
    [("A", "DT"), ("dog", "NN"), ("barks", "VBZ")],
    [("Birds", "NNS"), ("fly", "VBP")]
]

# Train the stochastic (probabilistic) tagger
tagger = UnigramTagger(train_data)

# Test sentence
sentence = "The cat sleeps"

words = word_tokenize(sentence)

# Predict POS tags
tagged = tagger.tag(words)

print("Stochastic POS Tagging:\n")

for word, tag in tagged:
    print(f"{word} --> {tag}")