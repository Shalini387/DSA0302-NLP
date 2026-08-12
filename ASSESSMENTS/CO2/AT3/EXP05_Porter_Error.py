import re
from nltk.stem import PorterStemmer

ps = PorterStemmer()

articles = [
    "The government announced new policies for economic growth.",
    "Companies are organizing new business operations.",
    "The technology organization developed new software.",
    "The communication system improved connectivity.",
    "The national government announced new changes."
]

print("ORIGINAL AND STEMMED WORDS")

for article in articles:
    words = re.findall(r'\b[a-zA-Z]+\b', article.lower())
    stems = [ps.stem(word) for word in words]

    print("\nOriginal :", " ".join(words))
    print("Stemmed  :", " ".join(stems))

print("\n20 STEMMING CASES")

words = [
    "organization",
    "organizer",
    "organizing",
    "organized",
    "connectivity",
    "nationality",
    "nationalize",
    "communication",
    "connection",
    "traditional",
    "conditional",
    "digitization",
    "washable",
    "hopeful",
    "relational",
    "easily",
    "fairly",
    "studies",
    "studied",
    "running"
]

for word in words:
    print(word, "->", ps.stem(word))