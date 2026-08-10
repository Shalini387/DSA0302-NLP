import math
from collections import Counter

corpus = [
    "data science is powerful",
    "data science drives innovation",
    "data science is evolving"
]

words = " ".join(corpus).lower().split()

unigram = Counter(words)
bigram = Counter(zip(words, words[1:]))
trigram = Counter(zip(words, words[1:], words[2:]))

print("SMART MOBILE KEYBOARD PREDICTION SYSTEM")
print("-" * 45)

# Q1: MLE Bigram
p1 = bigram[("data", "science")] / unigram["data"]

print("\n1. MLE Bigram Probability")
print("P(science | data) =", round(p1, 3))

# Q2: Backoff
if trigram[("data", "science", "improves")] > 0:
    p2 = trigram[("data", "science", "improves")] / bigram[("data", "science")]
    level = "Trigram"
elif bigram[("science", "improves")] > 0:
    p2 = bigram[("science", "improves")] / unigram["science"]
    level = "Bigram"
elif unigram["improves"] > 0:
    p2 = unigram["improves"] / len(words)
    level = "Unigram"
else:
    p2 = 0
    level = "No available n-gram"

print("\n2. Backoff Model")
print("Backoff Level =", level)
print("P(improves | data science) =", p2)

# Q3: Deleted Interpolation
p_tri = trigram[("data", "science", "is")] / bigram[("data", "science")]
p_bi = bigram[("science", "is")] / unigram["science"]
p_uni = unigram["is"] / len(words)

l1 = 0.5
l2 = 0.3
l3 = 0.2

p3 = l1 * p_tri + l2 * p_bi + l3 * p_uni

print("\n3. Deleted Interpolation")
print("Trigram =", round(p_tri, 3))
print("Bigram =", round(p_bi, 3))
print("Unigram =", round(p_uni, 3))
print("Interpolated Probability =", round(p3, 3))

# Q4: Entropy
p_is = 0.66
p_drives = 0.33

total = p_is + p_drives
p_is /= total
p_drives /= total

entropy = -(p_is * math.log2(p_is) +
            p_drives * math.log2(p_drives))

print("\n4. Entropy")
print("Entropy =", round(entropy, 3), "bits")