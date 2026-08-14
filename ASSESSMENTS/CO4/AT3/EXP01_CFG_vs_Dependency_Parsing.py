import nltk
import spacy

grammar = """
S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'The'
N -> 'doctor' | 'medicine'
V -> 'prescribed'
"""

cfg = nltk.CFG.fromstring(grammar)
parser = nltk.ChartParser(cfg)

sentence = "The doctor prescribed medicine".split()

print("CFG Tree:")
for tree in parser.parse(sentence):
    print(tree)

nlp = spacy.load("en_core_web_sm")
doc = nlp("The doctor prescribed medicine")

print("\nDependency Relations:")
for token in doc:
    print(token.text, "->", token.dep_, "->", token.head.text)