def plural_form(word):
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"
    elif word.endswith("y") and word[-2].lower() not in "aeiou":
        return word[:-1] + "ies"
    else:
        return word + "s"

word = "baby"

print("Singular Noun :", word)
print("Plural Noun   :", plural_form(word))