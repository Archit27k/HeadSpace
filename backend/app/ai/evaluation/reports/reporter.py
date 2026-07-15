import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class EvaluationReporter:
    """
    Aggregates metrics and generates regression reports.
    """
    def __init__(self, output_dir: str = "reports/"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.results = []
        
    def add_result(self, test_name: str, metrics: Dict[str, Any]):
        self.results.append({
            "test_name": test_name,
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    def generate_json_report(self) -> str:
        filepath = os.path.join(self.output_dir, f"eval_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=4)
        logger.info(f"Generated JSON report: {filepath}")
        return filepath
        
    def generate_markdown_report(self) -> str:
        filepath = os.path.join(self.output_dir, f"eval_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md")
        with open(filepath, 'w') as f:
            f.write("# AI Evaluation Regression Report\n\n")
            for res in self.results:
                f.write(f"## {res['test_name']}\n")
                f.write(f"- **Timestamp**: {res['timestamp']}\n")
                for k, v in res['metrics'].items():
                    f.write(f"- **{k}**: {v}\n")
                f.write("\n---\n")
        logger.info(f"Generated Markdown report: {filepath}")
        return filepath
