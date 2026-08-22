import re

text = (
    "The roads were flooded after heavy rainfall. "
    "Therefore, schools were closed for the day. "
    "Students attended classes online."
)

# Split text into sentences
sentences = re.split(r'(?<=[.!?])\s+', text.strip())

print("Sentences:")
for i, sentence in enumerate(sentences, 1):
    print(f"S{i}: {sentence}")

# Identify discourse relations
relations = []

if "Therefore" in sentences[1]:
    relations.append(("S1", "S2", "Cause-Effect"))

if "Students attended" in sentences[2] and "schools were closed" in sentences[1]:
    relations.append(("S2", "S3", "Result/Sequence"))

print("\nDiscourse Relations:")
for source, target, relation in relations:
    print(f"{source} -> {target}: {relation}")

# Coherence evaluation
coherence_score = len(relations) / (len(sentences) - 1)

print("\nCoherence Score:", coherence_score)

if coherence_score >= 0.5:
    print("Result: COHERENT")
else:
    print("Result: INCOHERENT")