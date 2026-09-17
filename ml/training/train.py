"""
Model Training Script for HireLens
Assigned to: Teammate 4 (Model Training)

Trains semantic similarity, classification, or ranking model on cleaned data
and exports the final artifact to saved_models/ for the backend team.
"""

import os
from pathlib import Path
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data_cleaning" / "processed" / "cleaned_resumes.csv"
SAVED_MODELS_DIR = BASE_DIR / "saved_models"

def train_baseline_model():
    """
    Starter baseline: Trains TF-IDF + Cosine Similarity or embedding pipeline.
    TODO: Replace with SentenceTransformers or fine-tuned BERT ranking model.
    """
    if not DATA_PATH.exists():
        print(f"Data file not found at: {DATA_PATH}")
        print("Please wait for Teammate 3 to finish data cleaning into processed/.")
        return

    print("Loading cleaned dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded with {len(df)} records.")

    # Example: Train TF-IDF vectorizer or SentenceTransformer
    # from sklearn.feature_extraction.text import TfidfVectorizer
    # vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    # X = vectorizer.fit_transform(df['cleaned_text'])

    # Export artifact for backend team:
    output_model_path = SAVED_MODELS_DIR / "resume_vectorizer.pkl"
    # joblib.dump(vectorizer, output_model_path)
    print(f"Model training pipeline ready. Export artifacts to {SAVED_MODELS_DIR}")

if __name__ == "__main__":
    train_baseline_model()
