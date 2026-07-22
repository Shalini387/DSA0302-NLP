import nltk
from nltk.tokenize import word_tokenize

text = "The quick brown fox jumps over the lazy dog."

words = word_tokenize(text)

pos_tags = nltk.pos_tag(words)

print("Part-of-Speech Tags:\n")

for word, tag in pos_tags:
    print(f"{word} --> {tag}")