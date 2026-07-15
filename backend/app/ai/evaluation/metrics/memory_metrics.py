from typing import Dict, Any

class MemoryMetrics:
    """
    Evaluates the quality of Memory Manager retrievals and summarizations.
    """
    
    @staticmethod
    def evaluate_injection(prompt: str, expected_fact: str) -> Dict[str, Any]:
        """
        Evaluates whether a specific fact was successfully injected into the prompt.
        """
        injected = expected_fact.lower() in prompt.lower()
        return {
            "metric": "memory_injection_rate",
            "score": 1.0 if injected else 0.0
        }
