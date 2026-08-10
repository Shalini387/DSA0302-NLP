import re
from collections import Counter

corpus = """
The student is studying natural language processing.
The student is learning machine learning.
The student is reading a book.
The student is writing a program.
The teacher is teaching natural language processing.
The teacher is reading a book.
The teacher is writing a program.
The student is learning Python.
The student is learning English.
The student is studying Python.
"""

tokens = re.findall(r'\b[a-z]+\b', corpus.lower())

unigrams = Counter(tokens)
bigrams = Counter(zip(tokens, tokens[1:]))
trigrams = Counter(zip(tokens, tokens[1:], tokens[2:]))

def get_probability(gram, n):
    if n == 1:
        return unigrams[gram] / len(tokens)
    elif n == 2:
        return bigrams[gram] / unigrams[gram[0]]
    else:
        return trigrams[gram] / bigrams[(gram[0], gram[1])]

def display_ngrams(n):
    data = unigrams if n == 1 else bigrams if n == 2 else trigrams

    print("\nN-gram Counts and Probabilities:")
    for gram, count in data.items():
        print(gram, ":", count, "->", round(get_probability(gram, n), 3))

def predict(sentence, n):
    words = re.findall(r'\b[a-z]+\b', sentence.lower())
    predictions = []

    for word in unigrams:
        if n == 1:
            gram = word
        elif n == 2:
            gram = (words[-1], word)
        else:
            if len(words) < 2:
                continue
            gram = (words[-2], words[-1], word)

        p = get_probability(gram, n)

        if p > 0:
            predictions.append((word, p))

    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:5]

n = int(input("Enter N (1, 2 or 3): "))
sentence = input("Enter incomplete sentence: ")

display_ngrams(n)

print("\nTop-5 Next Word Predictions:")
for word, p in predict(sentence, n):
    print(word, "->", round(p, 3))

print("\nUnseen N-gram Demonstration:")

if n == 1:
    gram = "computer"
elif n == 2:
    gram = ("student", "computer")
else:
    gram = ("student", "is", "computer")

print(gram, "->", get_probability(gram, n))

tests = [
    ("The student is", ["studying", "learning", "reading", "writing"]),
    ("The teacher is", ["teaching", "reading", "writing"])
]

correct = 0

for sentence, expected in tests:
    result = [w for w, p in predict(sentence, n)]
    if any(w in result for w in expected):
        correct += 1

accuracy = correct / len(tests) * 100

print("\nPrediction Accuracy:", round(accuracy, 2), "%")