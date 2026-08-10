import re
from collections import Counter

corpus = """
The student is studying natural language processing.
The student is learning machine learning.
The student is reading a book.
The student is writing a program.
The student is studying Python.
The student is learning Python.
The teacher is teaching natural language processing.
The teacher is reading a book.
The teacher is writing a program.
The teacher is learning Python.
The teacher is studying English.
The student is practicing English.
"""

tokens = re.findall(r'\b[a-z]+\b', corpus.lower())

uni = Counter(tokens)
bi = Counter(zip(tokens, tokens[1:]))
tri = Counter(zip(tokens, tokens[1:], tokens[2:]))

total = len(tokens)

def unigram(w):
    return uni[w] / total if uni[w] else 0

def bigram(w1, w2):
    return bi[(w1, w2)] / uni[w1] if bi[(w1, w2)] else 0

def trigram(w1, w2, w3):
    return tri[(w1, w2, w3)] / bi[(w1, w2)] if tri[(w1, w2, w3)] else 0

def unsmoothed(words, w):
    if len(words) >= 2:
        p = trigram(words[-2], words[-1], w)
        if p > 0:
            return p
    return 0

def backoff(words, w):
    if len(words) >= 2:
        p = trigram(words[-2], words[-1], w)
        if p > 0:
            return p

    p = bigram(words[-1], w)
    if p > 0:
        return p

    return unigram(w)

def interpolation(words, w):
    p1 = unigram(w)
    p2 = bigram(words[-1], w)

    p3 = 0
    if len(words) >= 2:
        p3 = trigram(words[-2], words[-1], w)

    return 0.2 * p1 + 0.3 * p2 + 0.5 * p3

def predict(sentence, model):
    words = re.findall(r'\b[a-z]+\b', sentence.lower())
    results = []

    for w in uni:
        if model == "unsmoothed":
            p = unsmoothed(words, w)
        elif model == "backoff":
            p = backoff(words, w)
        else:
            p = interpolation(words, w)

        results.append((w, p))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]

sentence = input("Enter sentence/query: ")

words = re.findall(r'\b[a-z]+\b', sentence.lower())

print("\nUNSEEN N-GRAM CHECK")

if len(words) >= 2:
    test = ("student", "is", "computer")
    print("Trigram:", test)
    print("Probability:", trigram(*test))

print("\nUNSMOOTHED MODEL")
for word, p in predict(sentence, "unsmoothed"):
    print(word, "->", round(p, 4))

print("\nBACKOFF MODEL")
for word, p in predict(sentence, "backoff"):
    print(word, "->", round(p, 4))

print("\nDELETED INTERPOLATION MODEL")
for word, p in predict(sentence, "interpolation"):
    print(word, "->", round(p, 4))