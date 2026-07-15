from typing import List, Dict, Any
from app.ai.prompts.base import BasePromptTemplate

class JournalIntelligencePrompt(BasePromptTemplate):
    """
    Prompt template for analyzing journal entries and extracting structured psychological insights.
    """
    
    @property
    def name(self) -> str:
        return "journal_intelligence"
        
    @property
    def description(self) -> str:
        return "Extracts structured psychological insights from a user's journal entry."
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def input_variables(self) -> List[str]:
        return ["journal_text"]
        
    def render(self, **kwargs) -> str:
        for var in self.input_variables:
            if var not in kwargs:
                raise ValueError(f"Missing required variable for {self.name}: {var}")
                
        template = f"""You are an expert clinical psychologist and AI journal analyzer.
Your task is to analyze the following journal entry and extract structured psychological insights.

<JOURNAL_ENTRY>
{kwargs['journal_text']}
</JOURNAL_ENTRY>

Perform a deep analysis and extract the following:
1. Summary: A concise summary of the entry.
2. Primary Emotions: The main emotions expressed.
3. Secondary Emotions: Subtle or underlying emotions.
4. Themes: Core themes discussed (e.g., 'Work Stress', 'Family', 'Self-Doubt').
5. Key Events: Major events described in the entry.
6. Stress Score: Estimate the user's stress level from 1 (lowest) to 10 (highest).
7. Cognitive Distortions: Identify any cognitive distortions (e.g., 'Catastrophizing', 'Black-and-white thinking', 'Filtering').
8. Reflection Questions: Generate 2-3 questions to help the user reflect deeper on this entry.
9. Recommended Coping Strategies: Suggest healthy coping mechanisms based on the entry.
10. Suggested Action Items: Provide actionable, small steps the user can take.
11. Memory Updates: Extract any facts, long-term preferences, recurring concerns, life goals, relationships, academic stress, career concerns, or health concerns that the AI should remember about the user.
12. Planner Metadata: Does this indicate severe distress or risk of harm requiring crisis intervention? Provide a suggested follow-up if applicable.

You must return the analysis strictly adhering to the requested JSON schema.
"""
        return template
