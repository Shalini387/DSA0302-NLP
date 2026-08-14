queries = {
    "Q1": ("ACTIVATE", "Roaming", "Activate Roaming"),
    "Q2": ("DEACTIVATE", "CallerTune", "Deactivate Caller Tune"),
    "Q3": ("QUERY", "DataBalance", "Query Data Balance"),
    "Q4": ("ACTIVATE", "5GService", "Activate 5G Service")
}

predicted = {
    "Q1": "Activate Roaming",
    "Q2": "Activate Caller Tune",
    "Q3": "Query Data Balance",
    "Q4": "Activate 5G Service"
}

for q, (action, obj, intent) in queries.items():
    representation = f"{action}({obj}, Customer)"
    result = "Correct" if intent == predicted[q] else "Incorrect"
    print(q, ":", representation, "->", result)