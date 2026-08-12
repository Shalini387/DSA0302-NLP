from nltk.stem import PorterStemmer

words = ["watches", "watching", "washable", "washer", "washed"]

stemmer = PorterStemmer()

print("WORD -> PORTER STEM")

for word in words:
    print(word, "->", stemmer.stem(word))

print("\nERROR ANALYSIS")

for word in words:
    stem = stemmer.stem(word)

    if word in ["watches", "watching", "washed"]:
        print(word, "->", stem, ": Inflectional")
    else:
        print(word, "->", stem, ": Derivational")