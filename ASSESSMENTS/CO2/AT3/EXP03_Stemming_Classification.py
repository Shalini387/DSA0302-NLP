import re
from nltk.stem import PorterStemmer, WordNetLemmatizer

texts = [
    "The organization is organizing a new technology system",
    "The company organized a technology conference",
    "The business organization appointed an organizer",
    "The technology company developed new software",
    "The business market showed strong financial growth",
    "The organization reported higher business revenue"
]

labels = ["tech", "tech", "business", "tech", "business", "business"]

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def clean(text):
    text = text.lower()
    text = re.sub(r"'s\b", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def stem(text):
    return " ".join(stemmer.stem(w) for w in clean(text).split())

def lemma(text):
    return " ".join(lemmatizer.lemmatize(w) for w in clean(text).split())

print("PORTER STEMMING RESULTS")

words = [
    "organization",
    "organizer",
    "organizing",
    "organized",
    "organization's"
]

for word in words:
    print(word, "->", stemmer.stem(word))

print("\nWITHOUT STEMMING")
for text in texts:
    print(clean(text))

print("\nPORTER STEMMING")
for text in texts:
    print(stem(text))

print("\nLEMMATIZATION")
for text in texts:
    print(lemma(text))