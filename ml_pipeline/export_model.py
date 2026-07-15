import os
import json
import joblib
import mlflow
from .config import config

def export_metadata(metadata: dict, run_id: str):
    """
    Saves the metadata to the local MLflow run as an artifact.
    """
    print(f"\nExporting metadata for {metadata['model_name']}...")
    
    # Export Metadata
    metadata_path = os.path.join(config.CACHE_DIR, "model_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)
        
    with mlflow.start_run(run_id=run_id):
        mlflow.log_artifact(metadata_path, "metadata")
        print("Logged model_metadata.json to MLflow run.")

