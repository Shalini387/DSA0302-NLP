# Constraint-Based Coreference Resolution

entities = {
    "John":  ("male", "singular", "animate"),
    "Mary":  ("female", "singular", "animate"),
    "ball":  ("neutral", "singular", "inanimate"),
    "dog":   ("neutral", "singular", "animate")
}

resolved = {
    "He": "John",
    "She": "Mary",
    "it": "ball",
    "him": "John",
    "they": "John + Mary + dog"
}

print("FINAL COREFERENCE RESOLUTION")
print("-" * 35)

for ref, antecedent in resolved.items():
    print(ref, "->", antecedent)

print("\nCOREFERENCE CHAINS")
print("-" * 35)

print("John : John -> He -> him -> they")
print("Mary : Mary -> She -> they")
print("Ball : ball -> it")
print("Dog  : dog -> they")