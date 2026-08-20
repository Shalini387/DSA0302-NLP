import nltk
from nltk import CFG
from nltk.parse import ChartParser
from nltk.corpus import wordnet

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'the' | 'a'
N -> 'student' | 'book' | 'teacher'
V -> 'reads' | 'teaches'
""")

parser = ChartParser(grammar)

sentence = input("Enter a sentence: ").lower().split()

trees = list(parser.parse(sentence))

print("\nSyntax-Driven Semantic Analysis")
print("--------------------------------")

if trees:
    tree = trees[0]
    print("\nParse Tree:")
    print(tree)

    print("\nNoun Phrases and Meanings:")

    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            phrase = " ".join(subtree.leaves())
            print("\nNoun Phrase:", phrase)

            meanings = []
            for word in subtree.leaves():
                synsets = wordnet.synsets(word, pos=wordnet.NOUN)

                if synsets:
                    meanings.append(
                        word + " : " + synsets[0].definition()
                    )

            for meaning in meanings:
                print(meaning)
else:
    print("Sentence cannot be parsed.")