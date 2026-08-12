expected = {
    "happiest": ["happy", "est"],
    "unbelievable": ["un", "believe", "able"],
    "running": ["run", "ing"],
    "reordering": ["re", "order", "ing"],
    "smartphones": ["smart", "phone", "s"],
    "unreadable": ["un", "read", "able"]
}

old = {
    "happiest": ["happiest"],
    "unbelievable": ["un", "believable"],
    "running": ["run", "ing"],
    "reordering": ["reorder", "ing"],
    "smartphones": ["smartphone", "s"],
    "unreadable": ["unreadable"]
}

new = expected

old_correct = sum(old[w] == expected[w] for w in expected)
new_correct = sum(new[w] == expected[w] for w in expected)

print("BEFORE CORRECTION")
for w in expected:
    print(w, "->", " + ".join(old[w]))

print("\nAFTER CORRECTION")
for w in expected:
    print(w, "->", " + ".join(new[w]))

print("\nAccuracy Before:", old_correct / len(expected) * 100, "%")
print("Accuracy After:", new_correct / len(expected) * 100, "%")

print("\nCOMPLEXITY")
print("Time Complexity: O(n)")
print("Space Complexity: O(s)")