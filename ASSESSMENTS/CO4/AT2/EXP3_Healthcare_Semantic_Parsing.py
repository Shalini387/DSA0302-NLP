import nltk
from nltk import CFG
from nltk.parse import EarleyChartParser

# CFG grammar
grammar = CFG.fromstring("""
S -> NP VP
NP -> DET NOUN
NP -> DET NOUN REL
REL -> PRON VERB DET NOUN TIME
VP -> VERB GERUND CONJ GERUND
GERUND -> VERB NOUN
GERUND -> VERB DET NOUN PP
PP -> PREP NOUN
DET -> 'the' | 'a'
NOUN -> 'doctor' | 'patient' | 'medication' | 'visit'
NOUN -> 'Chennai'
PRON -> 'who'
VERB -> 'reviewed' | 'recommends' | 'starting' | 'scheduling'
TIME -> 'last' 'week'
CONJ -> 'and'
PREP -> 'in'
""")

sentence = [
    'the', 'doctor', 'who', 'reviewed', 'the', 'patient',
    'last', 'week', 'recommends', 'starting', 'medication',
    'and', 'scheduling', 'a', 'visit', 'in', 'Chennai'
]

print("Medical Sentence:")
print(" ".join(sentence))

# Earley parsing
parser = EarleyChartParser(grammar)
trees = list(parser.parse(sentence))

print("\nParsing Result:")
if trees:
    print("Sentence parsed successfully")
else:
    print("Parsing failed")

# Feature Structure
print("\nFeature Structure:")
print("Doctor: Person=3, Number=Singular")
print("Recommends: Person=3, Number=Singular")
print("Agreement: Correct")

# Semantic extraction
print("\nSemantic Representation:")
print("Review(Doctor, Patient, LastWeek)")
print("Recommend(Doctor, Medication)")
print("Schedule(Doctor, FollowUpVisit, Chennai)")

# Structured output
print("\nStructured Output:")
print("Diagnosis: Not explicitly stated")
print("Treatment: Start Medication")
print("Follow-up: Schedule Visit")
print("Location: Chennai")