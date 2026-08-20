import nltk
from nltk import PCFG
from nltk.parse import ViterbiParser

grammar = PCFG.fromstring("""
S -> NP VP [1.0]
NP -> Det N [0.8]
NP -> Det N PP [0.2]
VP -> V NP [0.7]
VP -> V NP PP [0.3]
PP -> P NP [1.0]
Det -> 'the' [0.5]
Det -> 'a' [0.5]
N -> 'cat' [0.5]
N -> 'dog' [0.5]
V -> 'chased' [0.5]
V -> 'saw' [0.5]
P -> 'with' [1.0]
""")

parser = ViterbiParser(grammar)

sentence = input("Enter a sentence: ").lower().split()

print("\nMost Probable Parse Tree:\n")

trees = list(parser.parse(sentence))

if trees:
    for tree in trees:
        print(tree)
        print("\nProbability:", tree.prob())
else:
    print("No valid parse tree found.")