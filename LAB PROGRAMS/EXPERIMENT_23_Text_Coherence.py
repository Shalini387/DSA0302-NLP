import re
from collections import Counter

text = input("Enter a text: ")

sentences = re.split(r'[.!?]+', text)
sentences = [s.strip() for s in sentences if s.strip()]

words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

stopwords = {
    "the", "a", "an", "is", "are", "was", "were",
    "to", "of", "in", "on", "and", "for", "with",
    "this", "that", "it", "he", "she"
}

keywords = [word for word in words if word not in stopwords]
frequency = Counter(keywords)

score = 0

for i in range(len(sentences) - 1):
    words1 = set(re.findall(r'\b[a-zA-Z]+\b', sentences[i].lower()))
    words2 = set(re.findall(r'\b[a-zA-Z]+\b', sentences[i + 1].lower()))

    common = words1.intersection(words2)

    if common:
        score += 1

if len(sentences) > 1:
    coherence = (score / (len(sentences) - 1)) * 100
else:
    coherence = 100

print("\nText Coherence Evaluation")
print("-------------------------")
print("Number of Sentences:", len(sentences))
print("Common Keywords:", list(frequency.keys()))
print("Coherence Score:", round(coherence, 2), "%")

if coherence >= 50:
    print("Text is Coherent")
else:
    print("Text is Less Coherent")