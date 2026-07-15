import os
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from .config import config
from .dataset_loader import load_data
from .preprocessing import preprocess_dataframe
from .embedding_generator import EmbeddingGenerator
from .baseline_models import get_baseline_models
from .embedding_models import get_embedding_models
from .trainer import ModelTrainer
from .utils import generate_model_metadata
from .export_model import export_metadata
from .registry_client import RegistryClient

def run_shap_explainability(model, X_train, model_name, is_pipeline):
    """
    Runs SHAP explainability on classical models if applicable.
    Skips if it's too computationally expensive or unsupported.
    """
    print(f"Running SHAP explainability for {model_name}...")
    try:
        if is_pipeline:
            # We explain the classifier step, not the full TF-IDF pipeline easily
            # Getting feature names from TF-IDF
            tfidf = model.named_steps['tfidf']
            clf = model.named_steps['clf']
            X_transformed = tfidf.transform(X_train)
            feature_names = tfidf.get_feature_names_out()
            
            # Using a sample to speed up SHAP
            X_sample = shap.sample(X_transformed, 100)
            explainer = shap.Explainer(clf, X_sample, feature_names=feature_names)
            shap_values = explainer(X_sample)
            
            # Plot
            plt.figure()
            shap.summary_plot(shap_values, X_sample, feature_names=feature_names, show=False)
            plt.savefig(os.path.join(config.EXPLAINABILITY_DIR, f"{model_name}_shap_summary.png"))
            plt.close()
            print("SHAP explanation generated.")
        else:
            print("Skipping SHAP for dense embeddings (opaque dimensions).")
    except Exception as e:
        print(f"Skipping SHAP due to incompatibility: {e}")

def main():
    print("=== MLOps Benchmarking Suite ===")
    
    # 1. Data Loading & Preprocessing
    df, label_map = load_data()
    df = preprocess_dataframe(df)
    
    X = df['text']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=config.RANDOM_STATE)
    
    # 2. Embedding Generation
    embedding_gen = EmbeddingGenerator()
    X_train_emb = embedding_gen.generate(X_train.tolist())
    X_test_emb = embedding_gen.generate(X_test.tolist())
    
    # 3. Model Initialization
    baseline_models = get_baseline_models()
    embedding_models = get_embedding_models()
    trainer = ModelTrainer(label_map)
    
    results = []
    runs_info = [] # Store runs to later rank and register
    
    # 4. Pipeline A: Baseline TF-IDF
    for name, model in baseline_models.items():
        metrics, trained_model, run_id = trainer.train_and_evaluate(
            model_name=name, model=model,
            X_train=X_train.tolist(), y_train=y_train,
            X_test=X_test.tolist(), y_test=y_test,
            pipeline_type="Baseline", is_pipeline=True
        )
        results.append(metrics)
        runs_info.append({"name": f"Baseline_{name}", "metrics": metrics, "run_id": run_id, "is_pipeline": True})
        run_shap_explainability(trained_model, X_train.tolist(), f"Baseline_{name}", is_pipeline=True)

    # 5. Pipeline B: Dense Embeddings
    for name, model in embedding_models.items():
        metrics, trained_model, run_id = trainer.train_and_evaluate(
            model_name=name, model=model,
            X_train=X_train_emb, y_train=y_train,
            X_test=X_test_emb, y_test=y_test,
            pipeline_type="Primary", is_pipeline=False
        )
        results.append(metrics)
        runs_info.append({"name": f"Primary_{name}", "metrics": metrics, "run_id": run_id, "is_pipeline": False})
        run_shap_explainability(trained_model, X_train_emb, f"Primary_{name}", is_pipeline=False)

    # 6. Reporting
    results_df = pd.DataFrame(results).sort_values(by="F1_Score", ascending=False)
    
    # CSV
    results_df.to_csv(os.path.join(config.REPORTS_DIR, "benchmark_results.csv"), index=False)
    # JSON
    results_df.to_json(os.path.join(config.REPORTS_DIR, "benchmark_results.json"), orient="records", indent=4)
    # Markdown/CSV Summary
    results_df.to_csv(os.path.join(config.REPORTS_DIR, "benchmark_report.csv"), index=False)
    # HTML
    results_df.to_html(os.path.join(config.REPORTS_DIR, "benchmark_report.html"), index=False)

    print("\n=== Benchmarking Complete ===")
    print(results_df.to_string(index=False))
    
    # 7. Metadata and Registration Workflow
    registry = RegistryClient()
    
    # Sort runs by F1 > ROC-AUC > Inference Time > Size
    sorted_runs = sorted(runs_info, key=lambda x: (
        x["metrics"]["F1_Score"],
        x["metrics"]["ROC_AUC"] if x["metrics"]["ROC_AUC"] else 0,
        -x["metrics"]["Inference_Time_s"],
        -x["metrics"]["Model_Size_MB"]
    ), reverse=True)
    
    champion_info = sorted_runs[0]
    candidate_info = sorted_runs[1] if len(sorted_runs) > 1 else None

    def process_and_register(info, alias):
        run_id = info["run_id"]
        if registry.validate_run(run_id):
            metadata = generate_model_metadata(info["name"], info["metrics"], info["is_pipeline"])
            export_metadata(metadata, run_id)
            version = registry.register_model(run_id)
            registry.assign_alias(version, alias)
            print(f"Registered {info['name']} as {alias} (Version: {version})")
        else:
            print(f"Validation failed for {info['name']}. Cannot register as {alias}.")

    print("\n=== Registering Top Models ===")
    process_and_register(champion_info, "champion")
    if candidate_info:
        process_and_register(candidate_info, "candidate")

if __name__ == "__main__":
    main()
