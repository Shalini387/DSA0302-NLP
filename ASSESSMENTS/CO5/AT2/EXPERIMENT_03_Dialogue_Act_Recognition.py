import re

conversation = [
    ("User", "Can you book a train ticket for me?"),
    ("Agent", "Sure, where would you like to travel?"),
    ("User", "I want to go to Chennai."),
    ("Agent", "Your ticket has been booked.")
]

dialogue_acts = []

for speaker, utterance in conversation:
    text = utterance.lower()

    if speaker == "User" and ("book" in text or "can you" in text):
        act = "Request"

    elif "?" in utterance or "where" in text:
        act = "Question"

    elif speaker == "User" and ("i want" in text or "go to" in text):
        act = "Inform"

    elif "booked" in text:
        act = "Confirmation/Action"

    else:
        act = "Unknown"

    dialogue_acts.append((speaker, act))

print("Dialogue Acts:")
for speaker, act in dialogue_acts:
    print(f"{speaker}: {act}")

print("\nDialogue-Act Sequence:")
print(" → ".join(act for _, act in dialogue_acts))