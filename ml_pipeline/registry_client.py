import mlflow
from mlflow.tracking import MlflowClient
from .config import config

class RegistryClient:
    def __init__(self):
        mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
        self.client = MlflowClient()
        self.model_name = config.REGISTERED_MODEL_NAME
        
    def register_model(self, run_id: str):
        """
        Registers a model from a specific run_id.
        Returns the registered model version.
        """
        model_uri = f"runs:/{run_id}/model"
        result = mlflow.register_model(model_uri, self.model_name)
        return result.version
        
    def assign_alias(self, version: str, alias: str):
        """
        Assigns an alias (e.g., 'champion', 'candidate') to a specific version.
        """
        self.client.set_registered_model_alias(self.model_name, alias, version)
        print(f"Assigned alias '{alias}' to version {version} of {self.model_name}.")
        
    def delete_alias(self, alias: str):
        """
        Removes an alias.
        """
        try:
            self.client.delete_registered_model_alias(self.model_name, alias)
        except Exception as e:
            print(f"Alias {alias} not found or could not be deleted: {e}")

    def get_model_version_by_alias(self, alias: str):
        """
        Gets the version number assigned to an alias.
        """
        try:
            model_version_details = self.client.get_model_version_by_alias(self.model_name, alias)
            return model_version_details.version
        except Exception as e:
            return None

    def list_all_versions(self):
        """
        Returns a list of all versions for the registered model.
        """
        try:
            versions = self.client.search_model_versions(f"name='{self.model_name}'")
            return versions
        except Exception as e:
            return []

    def validate_run(self, run_id: str) -> bool:
        """
        Validates that a run has all necessary metrics, artifacts, and metadata
        before it can be registered.
        """
        run = self.client.get_run(run_id)
        metrics = run.data.metrics
        
        # Check essential metrics
        required_metrics = ["accuracy", "f1_score", "training_time_s", "inference_time_s"]
        for rm in required_metrics:
            if rm not in metrics:
                print(f"Validation failed: Missing metric '{rm}' in run {run_id}.")
                return False
                
        # Check model exists as an artifact (this checks if 'model' directory exists in artifacts)
        # mlflow.sklearn.log_model saves it under the 'model' path
        artifacts = [a.path for a in self.client.list_artifacts(run_id)]
        if "model" not in artifacts:
            print(f"Validation failed: No 'model' artifact found in run {run_id}.")
            return False
            
        return True
