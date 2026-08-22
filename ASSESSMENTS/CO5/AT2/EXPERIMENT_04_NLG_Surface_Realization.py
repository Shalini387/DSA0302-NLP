semantic_input = {
    "Action": "Buy",
    "Agent": "Student",
    "Object": "Book",
    "Tense": "Past"
}

# Lexical selection
agent = "the student"
action = semantic_input["Action"]
obj = "a book"

# Surface realization of tense
if semantic_input["Tense"] == "Past":
    verb = "bought"
else:
    verb = "buys"

# Sentence structuring
sentence = f"{agent} {verb} {obj}."

print("Semantic Input:", semantic_input)
print("Generated Sentence:", sentence)