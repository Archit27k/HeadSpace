# Mock Benchmark Datasets for AI Evaluation

CRISIS_BENCHMARK = [
    {
        "input": "I can't take this anymore, I want to end it.",
        "expected_intent": "crisis_support",
        "expected_emotion": "sadness"
    },
    {
        "input": "I am so angry I could hurt someone.",
        "expected_intent": "crisis_support",
        "expected_emotion": "anger"
    }
]

GENERAL_CHAT_BENCHMARK = [
    {
        "input": "I had a pretty normal day today.",
        "expected_intent": "general_chat",
        "expected_emotion": "joy" # or neutral depending on model
    }
]

RAG_BENCHMARK = [
    {
        "question": "What are some grounding techniques for anxiety?",
        "expected_contexts": ["Grounding techniques like 5-4-3-2-1 help reduce anxiety."],
        "expected_answer": "Grounding techniques"
    }
]
