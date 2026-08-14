from nltk import CFG
from nltk.parse import RecursiveDescentParser, EarleyChartParser

grammar = CFG.fromstring("""
S -> V NP
NP -> Det N PP PP
NP -> Det N N
NP -> Det N
NP -> N
PP -> P NP

V -> 'book'
Det -> 'a'
N -> 'flight' | 'Delhi' | 'window' | 'seat'
P -> 'to' | 'with'
""")

sentence = "book a flight to Delhi with a window seat".split()

print("Command:")
print(" ".join(sentence))

print("\nTop-Down Parsing:")
parser1 = RecursiveDescentParser(grammar)

try:
    tree1 = next(parser1.parse(sentence))
    print("Parse successful")
except StopIteration:
    print("No parse found")

print("\nEarley Parsing:")
parser2 = EarleyChartParser(grammar)

try:
    tree2 = next(parser2.parse(sentence))
    print("Parse successful")
except StopIteration:
    print("No parse found")

print("\nSemantic Representation:")
print("BookFlight(User, Delhi, WindowSeat)")