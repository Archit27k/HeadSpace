import logging
import os

logger = logging.getLogger(__name__)

class LangSmithClientWrapper:
    """
    Wraps the LangSmith SDK for dataset management and regression tracking.
    """
    def __init__(self):
        self.api_key = os.getenv("LANGCHAIN_API_KEY")
        try:
            from langsmith import Client
            if self.api_key:
                self.client = Client()
                logger.info("Initialized LangSmith Client")
            else:
                self.client = None
                logger.warning("LANGCHAIN_API_KEY not set. LangSmith running in mock mode.")
        except ImportError:
            self.client = None
            logger.warning("langsmith not installed. Running in mock mode.")

    def create_dataset(self, name: str, description: str):
        if self.client:
            try:
                return self.client.create_dataset(dataset_name=name, description=description)
            except Exception as e:
                logger.error(f"Failed to create dataset: {e}")
        return None
        
    def log_evaluation(self, run_name: str, metrics: dict):
        """
        In a full implementation, this logs custom metrics to a LangSmith run.
        """
        logger.info(f"Mock logging evaluation {run_name} to LangSmith: {metrics}")
