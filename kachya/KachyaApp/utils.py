from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_cosine_similarity(message, course_name):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([message] + course_name)
    cosine_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix).flatten()
    return cosine_similarity[1:]