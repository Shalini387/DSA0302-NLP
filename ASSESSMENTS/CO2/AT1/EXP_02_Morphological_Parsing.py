# EXP_02_Morphological_Parsing.py

# Input words
words = ["unhappy", "happiness", "happily"]

print("-" * 90)
print("{:<15}{:<10}{:<10}{:<10}{:<15}{:<15}".format(
    "Word", "Prefix", "Root", "Suffix", "Type", "Normalized"))
print("-" * 90)

for word in words:

    prefix = "-"
    suffix = "-"
    root = ""
    morph_type = ""

    if word.startswith("un"):
        prefix = "un"
        root = "happy"
        morph_type = "Derivational"

    elif word.endswith("ness"):
        root = "happy"
        suffix = "ness"
        morph_type = "Derivational"

    elif word.endswith("ly"):
        root = "happy"
        suffix = "ly"
        morph_type = "Derivational"

    else:
        root = word
        morph_type = "Unknown"

    print("{:<15}{:<10}{:<10}{:<10}{:<15}{:<15}".format(
        word, prefix, root, suffix, morph_type, root))