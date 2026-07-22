from nltk.tokenize import word_tokenize

# Input sentence
sentence = "The boy is playing happily"

# Tokenize the sentence
words = word_tokenize(sentence)

# Initial tagging (assume every word is a noun)
tags = [(word, "NN") for word in words]

# Apply transformation rules
new_tags = []

for word, tag in tags:
    if word.lower() in ["the", "a", "an"]:
        tag = "DT"
    elif word.lower() in ["is", "am", "are", "was", "were"]:
        tag = "VBZ"
    elif word.endswith("ing"):
        tag = "VBG"
    elif word.endswith("ly"):
        tag = "RB"

    new_tags.append((word, tag))

# Display output
print("Transformation-Based POS Tagging:\n")

for word, tag in new_tags:
    print(word, "-->", tag)