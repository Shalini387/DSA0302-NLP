# EXP_02_Morphological_Parsing.py

words = ["disagree", "agreement", "agreeable"]

print("-" * 120)
print("{:<15}{:<10}{:<12}{:<10}{:<15}{:<25}{:<12}".format(
    "Word", "Prefix", "Root", "Suffix",
    "Type", "Semantic Meaning", "Normalized"))
print("-" * 120)

for word in words:

    prefix = "-"
    suffix = "-"
    root = "agree"
    mtype = "Derivational"
    meaning = ""

    if word.startswith("dis"):
        prefix = "dis"
        meaning = "Negation (not agree)"

    elif word.endswith("ment"):
        suffix = "ment"
        meaning = "Action/State of agreeing"

    elif word.endswith("able"):
        suffix = "able"
        meaning = "Capable of agreeing"

    print("{:<15}{:<10}{:<12}{:<10}{:<15}{:<25}{:<12}".format(
        word, prefix, root, suffix,
        mtype, meaning, root))