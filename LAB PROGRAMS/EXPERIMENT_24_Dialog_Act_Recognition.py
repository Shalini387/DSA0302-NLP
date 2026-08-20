import re

text = input("Enter a dialog: ")

sentences = re.split(r'[.!?]+', text)

print("\nDialog Act Recognition")
print("---------------------")

for sentence in sentences:
    sentence = sentence.strip()

    if not sentence:
        continue

    if sentence.endswith("?"):
        act = "Question"
    elif re.search(r'\b(please|kindly|tell|give|show)\b', sentence.lower()):
        act = "Request"
    elif re.search(r'\b(hello|hi|hey|good morning|good evening)\b', sentence.lower()):
        act = "Greeting"
    elif re.search(r'\b(thank you|thanks)\b', sentence.lower()):
        act = "Thanking"
    elif re.search(r'\b(yes|okay|ok|sure)\b', sentence.lower()):
        act = "Agreement"
    else:
        act = "Statement"

    print("Dialog:", sentence)
    print("Act:", act)
    print()