import re
from collections import Counter

training = [
    [("the", "DT"), ("student", "NN"), ("reads", "VBZ"), ("a", "DT"), ("book", "NN")],
    [("the", "DT"), ("student", "NN"), ("studies", "VBZ"), ("python", "NN")],
    [("the", "DT"), ("teacher", "NN"), ("teaches", "VBZ"), ("english", "NN")],
    [("he", "PRP"), ("runs", "VBZ"), ("quickly", "RB")],
    [("she", "PRP"), ("writes", "VBZ"), ("a", "DT"), ("program", "NN")],
    [("the", "DT"), ("good", "JJ"), ("student", "NN"), ("learns", "VBZ")],
    [("the", "DT"), ("student", "NN"), ("is", "VBZ"), ("studying", "VBG")]
]

lexicon = {
    "the": "DT", "a": "DT", "an": "DT",
    "he": "PRP", "she": "PRP", "i": "PRP",
    "we": "PRP", "they": "PRP",
    "is": "VBZ", "am": "VBP", "are": "VBP",
    "reads": "VBZ", "studies": "VBZ", "teaches": "VBZ",
    "runs": "VBZ", "writes": "VBZ", "learns": "VBZ",
    "studying": "VBG", "reading": "VBG", "writing": "VBG",
    "student": "NN", "teacher": "NN", "book": "NN",
    "python": "NN", "english": "NN", "program": "NN",
    "good": "JJ", "quickly": "RB",
    "and": "CC", "in": "IN", "on": "IN", "with": "IN"
}

tags = ["NN", "VB", "VBZ", "VBG", "JJ", "RB", "PRP", "DT", "IN", "CC"]

word_tag = Counter()
tag_transition = Counter()
tag_count = Counter()

for sentence in training:
    previous = "<START>"

    for word, tag in sentence:
        word_tag[(word, tag)] += 1
        tag_count[tag] += 1
        tag_transition[(previous, tag)] += 1
        previous = tag

def rule_based(words):
    result = []

    for word in words:
        if word in lexicon:
            tag = lexicon[word]
        elif word.endswith("ing"):
            tag = "VBG"
        elif word.endswith("ly"):
            tag = "RB"
        elif word.endswith("ed"):
            tag = "VBD"
        elif word.endswith(("ous", "ful", "ive", "al")):
            tag = "JJ"
        else:
            tag = "NN"

        result.append((word, tag))

    return result

def stochastic(words):
    result = []
    previous = "<START>"

    for word in words:
        scores = {}

        for tag in tags:
            wt = word_tag[(word, tag)] + 1
            tt = tag_transition[(previous, tag)] + 1

            scores[tag] = wt * tt

        best_tag = max(scores, key=scores.get)
        result.append((word, best_tag))
        previous = best_tag

    return result

def transformation_based(result):
    result = result[:]

    for i, (word, tag) in enumerate(result):
        previous = result[i - 1][1] if i > 0 else ""

        if previous == "PRP" and tag == "NN":
            result[i] = (word, "VB")

        if previous in ("VBZ", "VBP") and tag == "NN":
            if word.endswith("ing"):
                result[i] = (word, "VBG")
            else:
                result[i] = (word, "VB")

        if word.endswith("ly"):
            result[i] = (word, "RB")

        if word.endswith("ing"):
            result[i] = (word, "VBG")

    return result

def display(title, result):
    print("\n" + title)
    for word, tag in result:
        print(word + "/" + tag, end=" ")
    print()

sentence = input("Enter an English sentence: ")
words = re.findall(r'\b[a-z]+\b', sentence.lower())

rule_result = rule_based(words)
stochastic_result = stochastic(words)
transformation_result = transformation_based(stochastic_result)

display("RULE-BASED TAGGING:", rule_result)
display("STOCHASTIC TAGGING:", stochastic_result)
display("TRANSFORMATION-BASED TAGGING:", transformation_result)