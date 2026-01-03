import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

COURSES = {
    "python": ["Coursera: Python for Everybody"],
    "machine learning": ["Coursera: ML by Andrew Ng"],
    "sql": ["Udemy: SQL Bootcamp"],
    "flask": ["Udemy: Flask Web Dev"]
}

class CareerModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2))
        self.model = MultinomialNB()
        self.career_skills = {
            "Data Scientist": ["python","statistics","machine learning","sql"],
            "Web Developer": ["html","css","javascript","flask"],
            "AI Engineer": ["python","deep learning","nlp"],
            "Cyber Security Analyst": ["networking","linux","security"]
        }

    def train_model(self, path):
        df = pd.read_csv(path)
        X = self.vectorizer.fit_transform(df["skills"])
        y = df["career"]
        self.model.fit(X, y)

    def predict_career(self, skills):
        v = self.vectorizer.transform([skills])
        p = self.model.predict_proba(v)[0]
        return sorted(zip(self.model.classes_, p), key=lambda x: x[1], reverse=True)
