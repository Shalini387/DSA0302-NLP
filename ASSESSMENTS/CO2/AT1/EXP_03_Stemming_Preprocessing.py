# EXP_03_Stemming_Preprocessing.py

# Input words
words = ["played", "player", "playing"]

print("-" * 90)
print("{:<15}{:<12}{:<15}{:<18}{:<15}".format(
    "Word", "Stem", "Removed Affix", "Type", "Normalized"))
print("-" * 90)

for word in words:

    stem = ""
    affix = "-"
    trans_type = ""

    if word.endswith("ed"):
        stem = word[:-2]
        affix = "ed"
        trans_type = "Inflectional"

    elif word.endswith("ing"):
        stem = word[:-3]
        affix = "ing"
        trans_type = "Inflectional"

    elif word.endswith("er"):
        stem = word[:-2]
        affix = "er"
        trans_type = "Derivational"

    else:
        stem = word
        trans_type = "Unknown"

    normalized = stem

    print("{:<15}{:<12}{:<15}{:<18}{:<15}".format(
        word, stem, affix, trans_type, normalized))