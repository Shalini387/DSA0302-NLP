import spacy

nlp = spacy.load("en_core_web_sm")

sentence = "The student reads a book."
doc = nlp(sentence)

print("Dependency Relations:")
for token in doc:
    print(token.text, "->", token.dep_, "->", token.head.text)