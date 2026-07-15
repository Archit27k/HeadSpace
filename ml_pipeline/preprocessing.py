import re
import string

def clean_text(text: str) -> str:
    """
    Cleans the input text for emotion classification.
    """
    if not isinstance(text, str):
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation (optional, depending on if punctuation holds emotional context)
    # text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_dataframe(df):
    """
    Applies text cleaning to the dataframe in place.
    """
    print("Preprocessing text data...")
    df['text'] = df['text'].apply(clean_text)
    # Remove rows that became empty after cleaning
    df = df[df['text'].astype(bool)]
    return df
