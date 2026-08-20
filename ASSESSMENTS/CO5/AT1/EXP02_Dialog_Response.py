# Constraint-Based Dialog Response Generation

responses = [
    "Take a short break and then return to your exam preparation with a clear focus. "
    "This can refresh your mind and help you concentrate better, so you can feel more confident.",

    "Try studying in short sessions with a small break between them so you can focus better on your exam. "
    "You can concentrate more effectively this way, and staying calm will help you feel confident.",

    "Take a short break, remove distractions, and give your full focus to the exam preparation. "
    "This will help you concentrate better and stay confident about what you have studied."
]

keywords = ["focus", "break", "confident"]

print("CONSTRAINT-BASED DIALOG RESPONSE")
print("=" * 40)

for i, response in enumerate(responses, 1):
    sentences = response.split(".")
    word_count = len(response.split())

    found = [word for word in keywords if word in response.lower()]

    print(f"\nResponse {i}:")
    print(response)
    print("Sentences:", len([s for s in sentences if s.strip()]))
    print("Keywords:", ", ".join(found))

    if 2 <= len([s for s in sentences if s.strip()]) <= 3 \
            and len(found) >= 2:
        print("Constraint Status: SATISFIED")
    else:
        print("Constraint Status: NOT SATISFIED")

print("\nBEST RESPONSE: Response 1")
print("Reason: It satisfies all constraints and gives clear")
print("advice followed by encouragement using a cause-effect relation.")