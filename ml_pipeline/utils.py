import os
import json
import sys
import subprocess
import datetime
import sklearn
import torch
import sentence_transformers
from .config import config

def get_git_revision_hash() -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except Exception:
        return "unknown"

def generate_model_metadata(model_name: str, metrics: dict, is_pipeline: bool) -> dict:
    metadata = {
        "model_name": model_name,
        "classifier": model_name.split("_")[-1],
        "embedding_model": "TF-IDF" if is_pipeline else config.EMBEDDING_MODEL,
        "dataset": config.DATASET_NAME,
        "training_date": datetime.datetime.utcnow().isoformat() + "Z",
        "git_commit_hash": get_git_revision_hash(),
        "python_version": sys.version,
        "sklearn_version": sklearn.__version__,
        "torch_version": torch.__version__,
        "sentence_transformers_version": sentence_transformers.__version__,
        "training_time": metrics.get("Training_Time_s"),
        "inference_time": metrics.get("Inference_Time_s"),
        "accuracy": metrics.get("Accuracy"),
        "precision": metrics.get("Precision"),
        "recall": metrics.get("Recall"),
        "f1": metrics.get("F1_Score"),
        "roc_auc": metrics.get("ROC_AUC"),
        "random_seed": config.RANDOM_STATE,
        "configuration": {
            "max_samples": config.MAX_SAMPLES,
            "batch_size": config.BATCH_SIZE,
            "device": config.DEVICE
        }
    }
    
    return metadata
