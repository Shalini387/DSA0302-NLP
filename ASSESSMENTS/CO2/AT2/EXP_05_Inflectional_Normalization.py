# EXP_05_Inflectional_Normalization.py

words = ["create", "creates", "creating"]

print("-" * 110)
print("{:<15}{:<10}{:<25}{:<12}{:<15}".format(
    "Word", "Suffix", "Grammatical Category",
    "Root", "Normalized"))
print("-" * 110)

for word in words:

    if word == "create":
        suffix = "-"
        category = "Base Form"

    elif word.endswith("s"):
        suffix = "s"
        category = "3rd Person Singular"

    elif word.endswith("ing"):
        suffix = "ing"
        category = "Present Participle"

    else:
        suffix = "-"
        category = "Unknown"

    root = "create"

    print("{:<15}{:<10}{:<25}{:<12}{:<15}".format(
        word, suffix, category, root, root))