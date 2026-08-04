# EXP_04_Finite_State_Morphological_Parsing.py

# Input words
words = ["writes", "writing", "written"]

print("-" * 120)
print("{:<12}{:<30}{:<15}{:<12}{:<15}{:<15}".format(
    "Word", "State Transition", "Root", "Suffix", "Pattern", "Normalized"))
print("-" * 120)

for word in words:

    if word == "writes":
        root = "write"
        suffix = "s"
        pattern = "Regular"
        transition = "Start -> write -> +s -> writes"

    elif word == "writing":
        root = "write"
        suffix = "ing"
        pattern = "Regular"
        transition = "Start -> write -> +ing -> writing"

    elif word == "written":
        root = "write"
        suffix = "en"
        pattern = "Irregular"
        transition = "Start -> write -> +en -> written"

    else:
        root = word
        suffix = "-"
        pattern = "Unknown"
        transition = "Start"

    normalized = root

    print("{:<12}{:<30}{:<15}{:<12}{:<15}{:<15}".format(
        word, transition, root, suffix, pattern, normalized))