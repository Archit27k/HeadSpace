from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from .config import config

def get_embedding_models():
    """
    Returns a dictionary of Pipeline B models that consume dense embeddings.
    Since embeddings are pre-computed, these are just the classifier components.
    """
    models = {
        "LR": LogisticRegression(max_iter=1000, random_state=config.RANDOM_STATE),
        "RF": RandomForestClassifier(n_estimators=100, random_state=config.RANDOM_STATE),
        "SVM": SVC(probability=True, random_state=config.RANDOM_STATE),
        "XGB": XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=config.RANDOM_STATE)
    }
    
    return {k: v for k, v in models.items() if k in config.CLASSIFIER_LIST}
