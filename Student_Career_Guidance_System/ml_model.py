import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

COURSES = {
    "python": ["Coursera: Python for Everybody"],
    "machine learning": ["Coursera: ML by Andrew Ng"],
    "sql": ["Udemy: SQL Bootcamp"],
    "flask": ["Udemy: Flask Web Development"]
}

class CareerModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        self.career_skills = {
            "Data Scientist": ["python", "statistics", "machine learning", "sql"],
            "Web Developer": ["html", "css", "javascript", "flask"],
            "AI Engineer": ["python", "deep learning", "nlp"],
            "Cyber Security Analyst": ["networking", "linux", "security"]
        }

    def train_model(self, path):
        df = pd.read_csv(path)
        X = self.vectorizer.fit_transform(df["skills"])
        y = df["career"]
        self.model.fit(X, y)

    def predict_career(self, skills):
        vec = self.vectorizer.transform([skills])
        probs = self.model.predict_proba(vec)[0]
        return sorted(zip(self.model.classes_, probs), key=lambda x: x[1], reverse=True)
