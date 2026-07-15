import os

class Config:
    # Experiment & Registry Tracking
    EXPERIMENT_NAME = "HeadSpace_Emotion_Classifier"
    REGISTERED_MODEL_NAME = "HeadSpace_Emotion_Model"
    
    # Dataset Configuration
    DATASET_NAME = "go_emotions" # Options: "go_emotions", "isear", "synthetic"
    TEXT_COLUMN = "text"
    LABEL_COLUMN = "label"
    MAX_SAMPLES = 5000 # Set to None for full dataset
    BATCH_SIZE = 32
    NUM_WORKERS = 4
    
    # Embedding Configuration
    # Options: "sentence-transformers/all-MiniLM-L6-v2", "BAAI/bge-small-en-v1.5", "intfloat/e5-base-v2"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2" 
    EMBEDDING_DIM = 384 # Adjust if using a different model

    # Classifiers to evaluate
    CLASSIFIER_LIST = ["LR", "RF", "SVM", "XGB"]
    
    # Export formats
    EXPORT_FORMATS = ["joblib", "onnx"]
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
    EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, "external")
    SYNTHETIC_DATA_DIR = os.path.join(DATA_DIR, "synthetic")
    CACHE_DIR = os.path.join(DATA_DIR, "cache")
    
    OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
    MODELS_DIR = os.path.join(OUTPUTS_DIR, "models")
    REPORTS_DIR = os.path.join(OUTPUTS_DIR, "reports")
    EXPLAINABILITY_DIR = os.path.join(OUTPUTS_DIR, "explainability")
    MLRUNS_DIR = os.path.join(OUTPUTS_DIR, "mlruns")
    
    # MLflow Tracking URI
    MLFLOW_TRACKING_URI = "sqlite:////tmp/mlflow.db"

    # Execution
    DEVICE = "cpu" # Options: "cpu", "cuda", "mps"
    RANDOM_SEED = 42
    RANDOM_STATE = 42

config = Config()
