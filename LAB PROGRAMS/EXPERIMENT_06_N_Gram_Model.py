import random
from nltk import bigrams
from collections import defaultdict

text = "I like Python I like NLP I like AI"

words = text.split()

model = defaultdict(list)

for w1, w2 in bigrams(words):
    model[w1].append(w2)

word = "I"
generated = [word]

for i in range(9):
    if word in model:
        word = random.choice(model[word])
        generated.append(word)
    else:
        break

print("Input Text:")
print(text)

print("\nGenerated Text:")
print(" ".join(generated))