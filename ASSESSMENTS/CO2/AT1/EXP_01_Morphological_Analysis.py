# EXP_01_Morphological_Analysis.py

# Input words
words = ["connected", "connecting", "connection"]

print("-" * 75)
print("{:<15}{:<12}{:<10}{:<18}{:<15}".format(
    "Word", "Root", "Suffix", "Type", "Normalized"))
print("-" * 75)

for word in words:

    if word.endswith("ed"):
        root = word[:-2]
        suffix = "ed"
        suffix_type = "Inflectional"

    elif word.endswith("ing"):
        root = word[:-3]
        suffix = "ing"
        suffix_type = "Inflectional"

    elif word.endswith("ion"):
        root = "connect"
        suffix = "ion"
        suffix_type = "Derivational"

    else:
        root = word
        suffix = "-"
        suffix_type = "Unknown"

    normalized = "connect"

    print("{:<15}{:<12}{:<10}{:<18}{:<15}".format(
        word, root, suffix, suffix_type, normalized))