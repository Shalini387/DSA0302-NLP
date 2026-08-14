import nltk
from nltk import CFG
from nltk.parse import EarleyChartParser

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N
VP -> V NP | V
Det -> 'The'
N -> 'student'
V -> 'wants'
""")

parser = EarleyChartParser(grammar)

sentence = "The student wants".split()

print("Earley Parsing Result:")
for tree in parser.parse(sentence):
    print(tree)