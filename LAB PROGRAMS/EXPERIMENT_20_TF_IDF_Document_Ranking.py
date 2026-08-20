from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "Python is easy to learn",
    "Python is used in artificial intelligence",
    "Java is a programming language"
]

query = input("Enter search query: ")

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

query_vector = vectorizer.transform([query])

similarity = cosine_similarity(query_vector, tfidf_matrix)[0]

ranking = sorted(
    enumerate(similarity, start=1),
    key=lambda x: x[1],
    reverse=True
)

print("\nDocument Ranking:")
for doc, score in ranking:
    print("Document", doc, "-->", round(score, 4))