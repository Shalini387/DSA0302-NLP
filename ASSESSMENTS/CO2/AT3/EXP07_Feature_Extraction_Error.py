import re
import time
from nltk.stem import PorterStemmer
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

stemmer = PorterStemmer()

data = fetch_20newsgroups(
    subset="train",
    categories=["sci.med", "sci.space"],
    remove=("headers", "footers", "quotes")
)

texts = data.data[:500]
labels = data.target[:500]

def stem_text(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return " ".join(stemmer.stem(word) for word in words)

split = 400

train_text = texts[:split]
test_text = texts[split:]
train_labels = labels[:split]
test_labels = labels[split:]

start = time.time()

vectorizer_before = CountVectorizer()
X_train_before = vectorizer_before.fit_transform(train_text)
X_test_before = vectorizer_before.transform(test_text)

model_before = LogisticRegression(max_iter=300)
model_before.fit(X_train_before, train_labels)

pred_before = model_before.predict(X_test_before)

time_before = time.time() - start

start = time.time()

train_stemmed = [stem_text(text) for text in train_text]
test_stemmed = [stem_text(text) for text in test_text]

vectorizer_after = CountVectorizer()
X_train_after = vectorizer_after.fit_transform(train_stemmed)
X_test_after = vectorizer_after.transform(test_stemmed)

model_after = LogisticRegression(max_iter=300)
model_after.fit(X_train_after, train_labels)

pred_after = model_after.predict(X_test_after)

time_after = time.time() - start

print("VOCABULARY AND CLASSIFICATION COMPARISON")

print("Vocabulary Before Stemming:",
      len(vectorizer_before.vocabulary_))

print("Vocabulary After Stemming:",
      len(vectorizer_after.vocabulary_))

print("Accuracy Before Stemming:",
      round(accuracy_score(test_labels, pred_before) * 100, 2), "%")

print("Accuracy After Stemming:",
      round(accuracy_score(test_labels, pred_after) * 100, 2), "%")

print("Processing Time Before:",
      round(time_before, 2), "seconds")

print("Processing Time After:",
      round(time_after, 2), "seconds")