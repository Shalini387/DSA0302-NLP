import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'the' | 'a'
N -> 'cat' | 'dog'
V -> 'chased' | 'saw'
""")

parser = RecursiveDescentParser(grammar)

sentence = input("Enter a sentence: ").lower().split()

print("\nTop-Down Parse Tree:\n")

trees = list(parser.parse(sentence))

if trees:
    for tree in trees:
        print(tree)
else:
    print("No valid parse tree found.")