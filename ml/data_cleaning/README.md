# ML Workspace: Data Cleaning & Feature Engineering

**Assigned to:**
- **Member 4:** Data Cleaning Specialist (Raw text cleaning, PII stripping, normalization)
- **Member 5:** Data & ML Hybrid (Feature engineering, skill vocabularies, training pair generation)

---

## Directory Layout
- `raw/`: Place raw downloaded datasets here (e.g. Kaggle Resume Dataset). *(Gitignored)*
- `processed/`: Save normalized, training-ready datasets here.
- `clean_resumes.py`: Data cleaning pipeline script (Owned by Member 4).
- `feature_engineering.py`: Feature extraction and dataset pairing script (Owned by Member 5).

---

## Task Division

### Member 4 (Data Cleaning Specialist)
1. Download target resume and job datasets into `raw/`.
2. Strip PII (emails, phone numbers, addresses, URLs).
3. Remove non-ASCII characters, HTML tags, and boilerplate headers/footers in `clean_resumes.py`.
4. Output clean text for Member 5.

### Member 5 (Data & ML Hybrid)
1. In `feature_engineering.py`, build domain skill dictionaries and tokenized text representations.
2. Form labeled Resume ↔ Job Description matching pairs (positive & negative samples).
3. Create training, validation, and test splits in `processed/`.
4. Partner with Member 6 (ML Engineer) to test data formats and features during model training.
