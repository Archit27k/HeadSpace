import pandas as pd
import numpy as np
from datasets import load_dataset
from .config import config

def load_data():
    """
    Loads dataset based on config.DATASET_NAME.
    Returns:
        pd.DataFrame with 'text' and 'label' columns.
        dict: mapping of integer labels to string names.
    """
    if config.DATASET_NAME == "go_emotions":
        print("Loading GoEmotions dataset from HuggingFace...")
        # Load simplified GoEmotions
        dataset = load_dataset("go_emotions", "simplified")
        df = dataset["train"].to_pandas()
        
        # GoEmotions has multiple labels per text, we simplify by taking the first one
        df['label'] = df['labels'].apply(lambda x: x[0] if len(x) > 0 else 27)
        df = df[['text', 'label']]
        
        # Get label mapping
        features = dataset["train"].features["labels"].feature
        label_names = features.names
        label_map = {idx: name for idx, name in enumerate(label_names)}
        
    elif config.DATASET_NAME == "synthetic":
        print("Generating synthetic dataset...")
        df, label_map = _generate_synthetic()
    else:
        raise ValueError(f"Dataset {config.DATASET_NAME} not supported yet.")

    # Limit samples if configured
    if config.MAX_SAMPLES and len(df) > config.MAX_SAMPLES:
        df = df.sample(n=config.MAX_SAMPLES, random_state=config.RANDOM_STATE)
    
    # Filter out empty texts
    df = df[df['text'].str.strip().astype(bool)]
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df, label_map

def _generate_synthetic():
    emotions = ["neutral", "happy", "sad", "anxious", "angry"]
    templates = {
        "neutral": ["I went to work today.", "The weather is okay."],
        "happy": ["I am so excited!", "Had a great time with friends."],
        "sad": ["I feel really down.", "Nothing seems to go right."],
        "anxious": ["I'm so worried.", "My heart is racing."],
        "angry": ["I am furious.", "This is so unfair!"]
    }
    
    np.random.seed(config.RANDOM_STATE)
    data = []
    num_samples = config.MAX_SAMPLES if config.MAX_SAMPLES else 1000
    
    for _ in range(num_samples):
        emotion = np.random.choice(emotions)
        text = np.random.choice(templates[emotion])
        data.append({"text": text, "label_str": emotion})
        
    df = pd.DataFrame(data)
    label_names = emotions
    label_map = {idx: name for idx, name in enumerate(label_names)}
    str_to_idx = {name: idx for idx, name in enumerate(label_names)}
    
    df['label'] = df['label_str'].map(str_to_idx)
    df = df[['text', 'label']]
    
    return df, label_map
