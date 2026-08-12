def parser(word):
    irregular = {
        "children": "child",
        "men": "man",
        "women": "woman",
        "mice": "mouse",
        "feet": "foot",
        "teeth": "tooth"
    }

    if word in irregular:
        return word, irregular[word], "Plural Noun"

    if word.endswith("ies"):
        return word, word[:-3] + "y", "Plural Noun"

    if word.endswith("es"):
        return word, word[:-2], "Plural Noun"

    if word.endswith("s"):
        return word, word[:-1], "Plural Noun"

    return word, word, "Singular"


words = ["cars", "boxes", "cities", "children"]

print("WORD -> ROOT -> TYPE")

for w in words:
    print(parser(w))