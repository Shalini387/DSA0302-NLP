from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

examples = ["cars", "children"]

print("Morphological Analysis - Example Words")
for word in examples:
    print(f"{word} --> {lemmatizer.lemmatize(word)}")

word = input("\nEnter a word for morphological analysis: ")

base_form = lemmatizer.lemmatize(word)

print("\nMorphological Analysis Result")
print("Original Word :", word)
print("Base Form     :", base_form)