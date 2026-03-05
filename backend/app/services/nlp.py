from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extract_topics(text: str, top_n: int = 40) -> list[dict]:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=500,
        ngram_range=(1, 1)
    )

    tfidf_matrix = vectorizer.fit_transform([text])
    scores = np.array(tfidf_matrix.todense()).flatten()
    words = vectorizer.get_feature_names_out()

    ranked = sorted(zip(words, scores), key=lambda x: x[1], reverse=True)
    ranked = [(w, s) for w, s in ranked if w.isalpha()]
    top_words = ranked[:top_n]

    # Normalize weights to a 0-1 range
    max_score = top_words[0][1] if top_words else 1
    return [
        {"word": word, "weight": round(float(score / max_score), 4)}
        for word, score in top_words
    ]