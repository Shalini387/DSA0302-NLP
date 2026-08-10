import re
import math
from collections import Counter

train = """
The student is studying natural language processing.
The student is learning machine learning.
The student is reading a book.
The teacher is teaching natural language processing.
The teacher is reading a book.
The teacher is learning Python.
The student is learning Python.
"""

test = """
The student is learning Python.
The teacher is reading a book.
The student is studying machine learning.
"""

def tokenize(text):
    return re.findall(r'\b[a-z]+\b', text.lower())

train_words = tokenize(train)
test_words = tokenize(test)

uni = Counter(train_words)
bi = Counter(zip(train_words, train_words[1:]))
tri = Counter(zip(train_words, train_words[1:], train_words[2:]))

V = len(set(train_words))

def unigram(w, smooth=False):
    if smooth:
        return (uni[w] + 1) / (len(train_words) + V)
    return uni[w] / len(train_words) if uni[w] else 0

def bigram(w1, w2, smooth=False):
    if smooth:
        return (bi[(w1, w2)] + 1) / (uni[w1] + V)
    return bi[(w1, w2)] / uni[w1] if bi[(w1, w2)] else 0

def trigram(w1, w2, w3, smooth=False):
    if smooth:
        return (tri[(w1, w2, w3)] + 1) / (bi[(w1, w2)] + V)
    return tri[(w1, w2, w3)] / bi[(w1, w2)] if tri[(w1, w2, w3)] else 0

def entropy(n, smooth=False):
    values = []

    for i, word in enumerate(test_words):
        if n == 1:
            p = unigram(word, smooth)
        elif n == 2:
            if i == 0:
                p = unigram(word, smooth)
            else:
                p = bigram(test_words[i-1], word, smooth)
        else:
            if i < 2:
                p = unigram(word, smooth)
            else:
                p = trigram(test_words[i-2], test_words[i-1], word, smooth)

        if p > 0:
            values.append(-math.log2(p))

    return sum(values) / len(values)

print("ENTROPY OF UNSMOOTHED MODELS")
print("Unigram :", round(entropy(1), 3))
print("Bigram  :", round(entropy(2), 3))
print("Trigram :", round(entropy(3), 3))

print("\nENTROPY AFTER LAP-LACE SMOOTHING")
print("Unigram :", round(entropy(1, True), 3))
print("Bigram  :", round(entropy(2, True), 3))
print("Trigram :", round(entropy(3, True), 3))

print("\nTEXT PREDICTION SCENARIO")

sentence = input("Enter word sequence: ")
words = tokenize(sentence)

candidates = []

for word in uni:
    if len(words) >= 2:
        p = trigram(words[-2], words[-1], word, True)
    elif len(words) == 1:
        p = bigram(words[-1], word, True)
    else:
        p = unigram(word, True)

    candidates.append((word, p))

candidates.sort(key=lambda x: x[1], reverse=True)

print("\nMost Predictable Next Words:")
for word, p in candidates[:5]:
    print(word, "->", round(p, 4))