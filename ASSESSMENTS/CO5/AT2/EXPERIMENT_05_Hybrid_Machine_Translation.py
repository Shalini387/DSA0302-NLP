source = "The boy is playing football."

# Step 1: Source analysis
interlingua = {
    "Agent": "BOY",
    "Action": "PLAY",
    "Object": "FOOTBALL",
    "Tense": "PRESENT_CONTINUOUS"
}

# Step 2: Candidate Tamil translations
candidates = {
    "சிறுவன் கால்பந்து விளையாடுகிறான்.": 0.935,
    "சிறுவன் கால்பந்து விளையாடுவான்.": 0.750,
    "பையன் கால்பந்து விளையாடுகிறான்.": 0.875
}

# Step 3: Statistical selection
best_translation = max(candidates, key=candidates.get)

print("Source Sentence:", source)
print("Interlingua Representation:", interlingua)

print("\nCandidate Translations:")
for sentence, score in candidates.items():
    print(f"{sentence} -> Score: {score}")

print("\nFinal Translation:")
print(best_translation)