sentences = {
    "Doctor prescribed medicine to patient":
        ["Doctor: Agent", "Medicine: Theme", "Patient: Recipient"],
    "Patient reported severe headache":
        ["Patient: Experiencer", "Headache: Symptom"],
    "Nurse monitored patient continuously":
        ["Nurse: Agent", "Patient: Theme"],
    "Medicine reduced blood pressure":
        ["Medicine: Cause", "Blood Pressure: Theme"]
}

for sentence, roles in sentences.items():
    print(sentence)
    for role in roles:
        print(role)
    print()