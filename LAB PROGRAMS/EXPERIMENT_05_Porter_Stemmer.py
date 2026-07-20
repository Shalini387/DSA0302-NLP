from nltk.stem import PorterStemmer

ps = PorterStemmer()

words = ["playing", "running", "studies", "happily", "connected"]

print("Original Word\tStemmed Word")

for word in words:
    print(word, "\t\t", ps.stem(word))