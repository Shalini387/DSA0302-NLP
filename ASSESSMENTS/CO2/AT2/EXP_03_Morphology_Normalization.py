# EXP_03_Morphology_Normalization.py

words = ["govern", "government", "governance"]

print("-" * 110)
print("{:<15}{:<12}{:<12}{:<20}{:<15}".format(
    "Word", "Root", "Affix", "Derivational Level", "Normalized"))
print("-" * 110)

for word in words:

    root = "govern"

    if word == "govern":
        affix = "-"
        level = "Base Word"

    elif word == "government":
        affix = "ment"
        level = "Level 1"

    elif word == "governance":
        affix = "ance"
        level = "Level 1"

    print("{:<15}{:<12}{:<12}{:<20}{:<15}".format(
        word, root, affix, level, root))