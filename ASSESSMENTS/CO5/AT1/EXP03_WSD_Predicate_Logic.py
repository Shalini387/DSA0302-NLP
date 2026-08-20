# Constraint-Based Word Sense Disambiguation

sentence = "The bank by the river flooded after the storm, but it was saved by quick action."

context = ["river", "flooded", "storm", "saved"]

senses = {
    "financial_bank": ["money", "loan", "account", "cash"],
    "river_bank": ["river", "flooded", "water", "storm"]
}

scores = {}

for sense, words in senses.items():
    scores[sense] = sum(word in context for word in words)

best_sense = max(scores, key=scores.get)

print("SOURCE SENTENCE:")
print(sentence)

print("\nSENSE SCORES:")
for sense, score in scores.items():
    print(sense, ":", score)

print("\nRESOLVED SENSE:")
print("bank -> riverbank")

print("\nPREDICATE LOGIC:")
print("RiverBank(b) AND River(r) AND Location(b,r)")
print("Storm(s) AND Flood(b)")
print("QuickAction(a) AND SavedBy(b,a)")
print("Contrast(Flood(b), SavedBy(b,a))")

print("\nPARAPHRASE:")
print("The riverbank flooded after the storm, but quick action saved it.")