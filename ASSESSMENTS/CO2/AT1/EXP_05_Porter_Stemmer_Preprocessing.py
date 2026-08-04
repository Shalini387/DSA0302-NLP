# EXP_05_Porter_Stemmer_Preprocessing.py

# Input words
words = ["relational", "relation", "relate"]

print("-" * 110)
print("{:<15}{:<20}{:<20}{:<15}{:<15}".format(
    "Word", "Applied Rule", "Intermediate", "Final Stem", "Normalized"))
print("-" * 110)

for word in words:

    if word == "relational":
        rule = "Remove 'ational'"
        intermediate = "relate"
        final_stem = "relat"

    elif word == "relation":
        rule = "Remove 'ion'"
        intermediate = "relat"
        final_stem = "relat"

    elif word == "relate":
        rule = "Remove final 'e'"
        intermediate = "relat"
        final_stem = "relat"

    else:
        rule = "-"
        intermediate = word
        final_stem = word

    print("{:<15}{:<20}{:<20}{:<15}{:<15}".format(
        word, rule, intermediate, final_stem, final_stem))