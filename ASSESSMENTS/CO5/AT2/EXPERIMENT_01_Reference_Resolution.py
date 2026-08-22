import re

text = "Ravi met Arun at the library. He borrowed a book and later returned it."

# Identify pronouns
pronouns = re.findall(r'\b(He|he|It|it|She|she|They|they)\b', text)

# Candidate entities found in the discourse
entities = ["Ravi", "Arun", "library", "book"]

# Reference resolution based on discourse and semantic context
resolution = {
    "He": "Ravi",
    "it": "book"
}

# Replace pronouns with resolved entities
resolved_text = text

for pronoun, entity in resolution.items():
    resolved_text = re.sub(
        rf'\b{pronoun}\b',
        entity,
        resolved_text
    )

print("Pronouns identified:", pronouns)
print("Reference Resolution:")

for pronoun, entity in resolution.items():
    print(f"{pronoun} -> {entity}")

print("\nResolved Discourse:")
print(resolved_text)