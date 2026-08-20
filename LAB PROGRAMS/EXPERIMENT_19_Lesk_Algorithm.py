import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk

sentence = input("Enter a sentence: ")
word = input("Enter the ambiguous word: ")

tokens = nltk.word_tokenize(sentence)

sense = lesk(tokens, word)

print("\nLesk Algorithm Result")
print("---------------------")

if sense:
    print("Word:", word)
    print("Selected Sense:", sense.name())
    print("Definition:", sense.definition())

    print("\nExamples:")
    for example in sense.examples():
        print("-", example)
else:
    print("No suitable sense found.")