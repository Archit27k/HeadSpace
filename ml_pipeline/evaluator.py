import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from .config import config

def evaluate_model(y_test, y_pred, y_prob, label_map, model_name, training_time, inference_time):
    """
    Evaluates the model and logs Accuracy, Precision, Recall, F1, ROC-AUC.
    """
    labels = [label_map[i] for i in range(len(label_map))]
    
    # Calculate metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    
    try:
        # Multi-class ROC-AUC
        roc_auc = roc_auc_score(y_test, y_prob, multi_class="ovr", average="weighted")
    except Exception:
        roc_auc = None

    metrics = {
        "Model": model_name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1_Score": f1,
        "ROC_AUC": roc_auc,
        "Training_Time_s": training_time,
        "Inference_Time_s": inference_time
    }
    
    # Classification Report
    report = classification_report(y_test, y_pred, labels=list(range(len(labels))), target_names=labels, output_dict=True, zero_division=0)
    report_df = pd.DataFrame(report).transpose()
    report_path = os.path.join(config.REPORTS_DIR, f"{model_name}_report.csv")
    report_df.to_csv(report_path)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.title(f'Confusion Matrix: {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    cm_path = os.path.join(config.REPORTS_DIR, f"{model_name}_cm.png")
    plt.savefig(cm_path)
    plt.close()
    
    return metrics, cm_path, report_path
