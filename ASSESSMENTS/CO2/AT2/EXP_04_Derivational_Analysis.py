# EXP_04_Derivational_Analysis.py

words = ["activate", "activation", "reactivation"]

print("-" * 125)
print("{:<15}{:<10}{:<12}{:<10}{:<25}{:<15}".format(
    "Word", "Prefix", "Root", "Suffix",
    "Derivational Sequence", "Normalized"))
print("-" * 125)

for word in words:

    prefix = "-"
    root = "activate"
    suffix = "-"
    sequence = "Base"

    if word == "activation":
        suffix = "ion"
        sequence = "activate → activation"

    elif word == "reactivation":
        prefix = "re"
        suffix = "ion"
        sequence = "activate → activation → reactivation"

    print("{:<15}{:<10}{:<12}{:<10}{:<25}{:<15}".format(
        word, prefix, root, suffix, sequence, root))