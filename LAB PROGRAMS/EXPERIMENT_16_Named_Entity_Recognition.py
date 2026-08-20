import spacy

nlp = spacy.load("en_core_web_sm")

text = input("Enter a sentence: ")

doc = nlp(text)

print("\nNamed Entities:\n")

if doc.ents:
    for entity in doc.ents:
        print(entity.text, "-->", entity.label_)
else:
    print("No named entities found.")