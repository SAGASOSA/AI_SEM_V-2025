# recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class NewsRecommender:
    def __init__(self, csv_path="data/election_news.csv", beta=0.0):
        self.data = pd.read_csv(csv_path)
        self.beta = beta  # algorithmic bias: -1 (left) → +1 (right)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.data['headline'])
    
    def recommend(self, query, top_n=5):
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        scores = sims.copy()

        # Introduce bias
        for i, bias in enumerate(self.data['political_bias']):
            if bias == "right":
                scores[i] *= (1 + self.beta)
            elif bias == "left":
                scores[i] *= (1 - self.beta)
            # neutral unchanged

        top_indices = scores.argsort()[-top_n:][::-1]
        return self.data.iloc[top_indices][['headline','topic','political_bias','source']]
