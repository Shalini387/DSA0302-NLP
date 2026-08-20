import re

text = input("Enter a text: ")

sentences = re.split(r'[.!?]', text)

entities = []
pronouns = ["he", "she", "it", "they", "him", "her", "them"]

print("\nReference Resolution")
print("--------------------")

for sentence in sentences:
    words = sentence.strip().split()

    for word in words:
        clean_word = re.sub(r'[^a-zA-Z]', '', word)

        if clean_word.lower() in pronouns:
            if entities:
                print(clean_word, "-->", entities[-1])
        elif clean_word:
            if clean_word[0].isupper():
                entities.append(clean_word)