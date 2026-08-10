from collections import Counter
import math

sentence = ["economic", "growth", "increases", "employment"]
tags = ["JJ", "NN", "NNS", "NN"]

print("NEWS ANALYTICS AND POS TAG CORRECTION")
print("-" * 45)

print("\nInitial Tags:")
for word, tag in zip(sentence, tags):
    print(word + "/" + tag)

for i in range(1, len(tags)):
    if tags[i] == "NNS" and tags[i - 1] == "NN":
        tags[i] = "VBZ"

print("\nCorrected Tags:")
for word, tag in zip(sentence, tags):
    print(word + "/" + tag)

freq = {
    "economic": 120,
    "growth": 450,
    "increases": 210,
    "employment": 380
}

total = sum(freq.values())

print("\nWord Frequency Distribution:")
for word, count in freq.items():
    probability = count / total
    print(word, ":", count, "Probability =", round(probability, 4))

p1 = 0.5
p2 = 0.5

entropy_before = -(p1 * math.log2(p1) +
                   p2 * math.log2(p2))

entropy_after = 0

print("\nEntropy Before =", round(entropy_before, 3), "bits")
print("Entropy After =", entropy_after, "bits")