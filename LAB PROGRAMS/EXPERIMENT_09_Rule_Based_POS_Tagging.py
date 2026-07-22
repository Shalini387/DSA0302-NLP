import nltk
from nltk.tag import RegexpTagger
from nltk.tokenize import word_tokenize

patterns = [
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*es$', 'VBZ'),
    (r'.*ly$', 'RB'),
    (r'.*ous$', 'JJ'),
    (r'.*s$', 'NNS'),
    (r'^[0-9]+$', 'CD'),
    (r'.*', 'NN')
]

tagger = RegexpTagger(patterns)

sentence = "The students are studying happily"

words = word_tokenize(sentence)

tagged = tagger.tag(words)

print("Rule-Based POS Tagging:\n")

for word, tag in tagged:
    print(f"{word} --> {tag}")