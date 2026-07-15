import mlflow
import time
import os
from .evaluator import evaluate_model
from .config import config

class ModelTrainer:
    def __init__(self, label_map):
        self.label_map = label_map
        mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(config.EXPERIMENT_NAME)

    def train_and_evaluate(self, model_name: str, model, X_train, y_train, X_test, y_test, pipeline_type: str, is_pipeline: bool):
        """
        Trains and evaluates a model, tracking everything with MLflow.
        """
        print(f"\n--- Training {pipeline_type}: {model_name} ---")
        
        with mlflow.start_run(run_name=f"{pipeline_type}_{model_name}") as run:
            # Log params
            mlflow.log_param("model_name", model_name)
            mlflow.log_param("pipeline_type", pipeline_type)
            mlflow.log_param("dataset", config.DATASET_NAME)
            mlflow.log_param("is_pipeline", is_pipeline)
            if not is_pipeline:
                mlflow.log_param("embedding_model", config.EMBEDDING_MODEL)

            # Train
            start_train = time.time()
            model.fit(X_train, y_train)
            train_time = time.time() - start_train
            
            # Predict
            start_infer = time.time()
            y_pred = model.predict(X_test)
            try:
                y_prob = model.predict_proba(X_test)
            except AttributeError:
                y_prob = None
            infer_time = time.time() - start_infer

            # Evaluate
            metrics, cm_path, report_path = evaluate_model(
                y_test, y_pred, y_prob, self.label_map, f"{pipeline_type}_{model_name}", 
                train_time, infer_time
            )
            
            # Log metrics
            mlflow.log_metric("accuracy", metrics["Accuracy"])
            mlflow.log_metric("f1_score", metrics["F1_Score"])
            mlflow.log_metric("precision", metrics["Precision"])
            mlflow.log_metric("recall", metrics["Recall"])
            if metrics["ROC_AUC"] is not None:
                mlflow.log_metric("roc_auc", metrics["ROC_AUC"])
            mlflow.log_metric("training_time_s", train_time)
            mlflow.log_metric("inference_time_s", infer_time)
            
            # Log artifacts
            mlflow.log_artifact(cm_path)
            mlflow.log_artifact(report_path)
            
            # Use MLflow's native sklearn logging to properly save the model
            # This is essential for Model Registry compatibility
            from mlflow.models.signature import infer_signature
            signature = infer_signature(X_train[:5], y_pred[:5])
            
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                signature=signature,
                input_example=X_train[:1]
            )
            
            # Calculate rough model size
            import joblib
            temp_path = os.path.join(config.CACHE_DIR, f"temp_{model_name}.joblib")
            joblib.dump(model, temp_path)
            size_mb = os.path.getsize(temp_path) / (1024 * 1024)
            os.remove(temp_path)
            
            metrics["Model_Size_MB"] = size_mb
            mlflow.log_metric("model_size_mb", size_mb)
            
            print(f"Accuracy: {metrics['Accuracy']:.4f} | F1: {metrics['F1_Score']:.4f}")
            
            # Return metrics, the trained model, and the MLflow run_id
            return metrics, model, run.info.run_id
