# EXP_01_Morphological_Analysis.py

words = ["analyzing", "analysis", "analytical"]

print("-" * 90)
print("{:<15}{:<12}{:<12}{:<15}{:<15}".format(
    "Word", "Root", "Affix", "Type", "Normalized"))
print("-" * 90)

for word in words:

    if word.endswith("ing"):
        root = "analyze"
        affix = "ing"
        mtype = "Inflectional"

    elif word.endswith("sis"):
        root = "analyze"
        affix = "sis"
        mtype = "Derivational"

    elif word.endswith("ical"):
        root = "analyze"
        affix = "ical"
        mtype = "Derivational"

    else:
        root = word
        affix = "-"
        mtype = "Unknown"

    normalized = "analyze"

    print("{:<15}{:<12}{:<12}{:<15}{:<15}".format(
        word, root, affix, mtype, normalized))