import time
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from config import config
from dataset_loader import load_data
from preprocessing import preprocess_dataframe
from embedding_generator import EmbeddingGenerator
from baseline_models import get_baseline_models
from embedding_models import get_embedding_models
from evaluate import evaluate_model
from export_model import export_best_model

def main():
    print(f"Starting ML Benchmarking Pipeline")
    print(f"Dataset: {config.DATASET_NAME}")
    
    # 1. Load Data
    df, label_map = load_data()
    print(f"Loaded {len(df)} samples.")
    
    # 2. Preprocessing
    df = preprocess_dataframe(df)
    
    X = df['text']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=config.RANDOM_STATE)
    
    # 3. Generate Embeddings for Pipeline B
    embedding_gen = EmbeddingGenerator()
    X_train_emb = embedding_gen.generate(X_train.tolist())
    X_test_emb = embedding_gen.generate(X_test.tolist())
    
    # 4. Initialize Models
    baseline_models = get_baseline_models()
    embedding_models = get_embedding_models()
    
    results = []
    best_f1 = 0
    best_model = None
    best_model_name = None
    best_is_pipeline = False
    
    # Save label map for inference
    joblib.dump(label_map, os.path.join(config.MODELS_DIR, "label_map.joblib"))
    
    # Helper to train and evaluate
    def train_and_eval(name, model, train_data, test_data, is_pipeline):
        nonlocal best_f1, best_model, best_model_name, best_is_pipeline
        
        print(f"\n--- Training {name} ---")
        start_train = time.time()
        model.fit(train_data, y_train)
        train_time = time.time() - start_train
        
        start_infer = time.time()
        y_pred = model.predict(test_data)
        y_prob = model.predict_proba(test_data)
        infer_time = time.time() - start_infer
        
        # Calculate model size roughly by serializing to joblib temporarily
        temp_path = os.path.join(config.MODELS_DIR, f"temp_{name}.joblib")
        joblib.dump(model, temp_path)
        size_mb = os.path.getsize(temp_path) / (1024 * 1024)
        os.remove(temp_path)
        
        metrics = evaluate_model(
            y_test, y_pred, y_prob, label_map, name, 
            train_time, infer_time, size_mb
        )
        
        results.append(metrics)
        print(f"Accuracy: {metrics['Accuracy']:.4f} | F1: {metrics['F1_Score']:.4f} | ROC-AUC: {metrics['ROC_AUC']}")
        
        if metrics['F1_Score'] > best_f1:
            best_f1 = metrics['F1_Score']
            best_model = model
            best_model_name = name
            best_is_pipeline = is_pipeline

    # 5. Run Pipeline A (Baseline TF-IDF)
    print("\n=== Pipeline A: TF-IDF Baseline ===")
    for name, model in baseline_models.items():
        # Scikit-learn TF-IDF pipelines need arrays of strings, not pandas Series with index
        train_and_eval(name, model, X_train.tolist(), X_test.tolist(), is_pipeline=True)
        
    # 6. Run Pipeline B (Dense Embeddings)
    print("\n=== Pipeline B: Dense Embeddings ===")
    for name, model in embedding_models.items():
        train_and_eval(name, model, X_train_emb, X_test_emb, is_pipeline=False)
        
    # 7. Summary
    results_df = pd.DataFrame(results)
    print("\n=== Benchmarking Summary ===")
    print(results_df.sort_values(by="F1_Score", ascending=False).to_string(index=False))
    
    results_df.to_csv(os.path.join(config.REPORTS_DIR, "benchmark_results.csv"), index=False)
    
    # 8. Export Best Model
    print(f"\nBest Model: {best_model_name} with F1 = {best_f1:.4f}")
    export_best_model(best_model, best_model_name, is_pipeline=best_is_pipeline)
    
if __name__ == "__main__":
    main()
