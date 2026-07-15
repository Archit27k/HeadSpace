from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from .config import config

def get_baseline_models():
    """
    Returns a dictionary of Pipeline A (TF-IDF + Classifier) models.
    """
    tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
    
    models = {
        "LR": Pipeline([
            ("tfidf", tfidf),
            ("clf", LogisticRegression(max_iter=1000, random_state=config.RANDOM_STATE))
        ]),
        "RF": Pipeline([
            ("tfidf", tfidf),
            ("clf", RandomForestClassifier(n_estimators=100, random_state=config.RANDOM_STATE))
        ]),
        "SVM": Pipeline([
            ("tfidf", tfidf),
            ("clf", SVC(probability=True, random_state=config.RANDOM_STATE))
        ]),
        "XGB": Pipeline([
            ("tfidf", tfidf),
            ("clf", XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=config.RANDOM_STATE))
        ])
    }
    
    return {k: v for k, v in models.items() if k in config.CLASSIFIER_LIST}
