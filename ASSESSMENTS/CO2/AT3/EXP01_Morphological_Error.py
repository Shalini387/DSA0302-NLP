import re
from nltk.stem import PorterStemmer

text = """
Infection is common in infectious diseases.
The patient was infected with a bacterial infection.
Researchers investigate infectious conditions.
"""

words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

stemmer = PorterStemmer()

print("PREPROCESSED WORDS")
print(words)

print("\nPORTER STEMMING RESULTS")

for word in ["infect", "infection", "infectious", "infected"]:
    print(word, "->", stemmer.stem(word))