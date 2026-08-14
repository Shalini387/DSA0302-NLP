import nltk
import spacy
from nltk import CFG, PCFG
from nltk.parse import ChartParser, ViterbiParser

sentence = "She saw the man with a telescope".split()

print("SENTENCE:")
print(" ".join(sentence))

# CFG
cfg_grammar = CFG.fromstring("""
S -> NP VP
NP -> Pronoun | Det N | Det N PP
VP -> V NP | V NP PP
PP -> P NP
Pronoun -> 'She'
Det -> 'the' | 'a'
N -> 'man' | 'telescope'
V -> 'saw'
P -> 'with'
""")

cfg_parser = ChartParser(cfg_grammar)

print("\nCFG PARSE TREES:")

count = 0
for tree in cfg_parser.parse(sentence):
    print(tree)
    count += 1

print("Number of CFG parses:", count)

# PCFG
pcfg_grammar = PCFG.fromstring("""
S -> NP VP [1.0]
NP -> Pronoun [0.2]
NP -> Det N [0.5]
NP -> Det N PP [0.3]
VP -> V NP [0.6]
VP -> V NP PP [0.4]
PP -> P NP [1.0]
Pronoun -> 'She' [1.0]
Det -> 'the' [0.6]
Det -> 'a' [0.4]
N -> 'man' [0.6]
N -> 'telescope' [0.4]
V -> 'saw' [1.0]
P -> 'with' [1.0]
""")

pcfg_parser = ViterbiParser(pcfg_grammar)

print("\nPCFG MOST PROBABLE PARSE:")

for tree in pcfg_parser.parse(sentence):
    print(tree)
    print("Probability:", tree.prob())
    break

# Neural Parsing
print("\nNEURAL DEPENDENCY PARSING:")

nlp = spacy.load("en_core_web_sm")
doc = nlp("She saw the man with a telescope")

for token in doc:
    print(token.text, "->", token.dep_, "->", token.head.text)