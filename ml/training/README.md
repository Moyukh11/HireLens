# ML Workspace: Model Training & Evaluation

**Assigned to:**
- **Member 6:** ML Model Engineer (Lead: Model architecture, training pipeline, evaluation)
- **Member 5:** Data & ML Hybrid (Collaborator: Experimentation in `notebooks/`, feature tuning)

---

## Directory Layout
- `notebooks/`: Jupyter notebooks for exploratory data analysis (EDA) and model experimentation.
- `train.py`: Main reproducible training and pipeline export script (Owned by Member 6).
- `evaluate.py`: Evaluation metrics (Cosine similarity distributions, Top-K ranking accuracy).
- `saved_models/`: **CRITICAL INTEGRATION POINT** — Export your trained model weights here.

---

## Task Division

### Member 6 (Lead ML Engineer)
1. **Model Architecture:**
   - **Option A (Sentence-BERT):** Use `sentence-transformers/all-MiniLM-L6-v2` to compute dense embeddings for resumes and JDs and calculate Cosine Similarity.
   - **Option B (TF-IDF + Classifier):** Fit TF-IDF Vectorizer + Cosine Similarity + Classifier (XGBoost / Logistic Regression).
2. **Evaluation:**
   - Benchmark models in `evaluate.py` using ranking precision and similarity thresholds.
3. **Model Export:**
   - Save model weights to `saved_models/` and document expected input/output formats for Member 3 (Backend Dev 2).

### Member 5 (Data & ML Hybrid)
1. Partner with Member 6 in `notebooks/` to validate features and experiment with different vectorization methods.
2. Ensure training data format from `ml/data_cleaning/processed/` matches the model's required input schema.
