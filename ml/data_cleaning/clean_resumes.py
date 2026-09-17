"""
Dataset Cleaning & Preprocessing Script for HireLens
Assigned to: Teammate 3 (Dataset Cleaning)

Run this script to clean raw resume/job datasets and output normalized data to processed/.
"""

import os
import re
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

def clean_text(text: str) -> str:
    """Removes special characters, extra whitespace, and common noise."""
    if not isinstance(text, str):
        return ""
    # Normalize unicode / whitespace
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    # Remove emails
    text = re.sub(r'\S+@\S+', ' ', text)
    # Remove non-ascii or excessive punctuation
    text = re.sub(r'[^\w\s\+\#\.]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_dataset(input_filename: str, output_filename: str):
    input_path = RAW_DIR / input_filename
    output_path = PROCESSED_DIR / output_filename
    
    if not input_path.exists():
        print(f"File not found: {input_path}")
        print(f"Please place your raw CSV/JSON file in {RAW_DIR}")
        return

    print(f"Loading raw dataset from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Example cleaning pipeline:
    # df['cleaned_text'] = df['Resume_str'].apply(clean_text)
    
    print(f"Saving cleaned dataset to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Data cleaning complete!")

if __name__ == "__main__":
    # Example usage:
    # process_dataset("UpdatedResumeDataSet.csv", "cleaned_resumes.csv")
    print("HireLens Data Cleaning Pipeline Ready.")
    print(f"Drop raw files in: {RAW_DIR}")
