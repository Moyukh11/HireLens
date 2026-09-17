# HireLens — AI-Powered Resume Screener & Job Matcher

HireLens is an intelligent candidate screening and job matching platform that parses resumes, analyzes job descriptions, and provides explainable, ML-driven candidate rankings.

---

## 👥 Team Roles & Workspaces

The codebase is organized into isolated modules tailored to each team member's role:

```text
HireLens/
├── frontend/             # [Frontend Engineer] Streamlit UI & Candidate Dashboard
├── backend/              # [Backend Engineers (2)] FastAPI, REST API & Model Serving
├── ml/
│   ├── data_cleaning/    # [Data Engineer] Dataset collection, PII stripping & cleaning
│   └── training/         # [ML Engineer] Model training, evaluation & artifact export
└── README.md
```

| Role | Assignee | Folder | Key Responsibilities |
|---|---|---|---|
| **Frontend** | Member 1 | [`frontend/`](./frontend) | Streamlit dashboard, upload interfaces, score visualizations |
| **Backend** | Member 2 & Member 3 | [`backend/`](./backend) | FastAPI service, candidate persistence, parser & model integration |
| **Data Cleaning** | Member 4 & Member 5 | [`ml/data_cleaning/`](./ml/data_cleaning) | Dataset acquisition, normalization, text cleaning, feature engineering |
| **Model Training**| Member 5 & Member 6 | [`ml/training/`](./ml/training) | Semantic embeddings / NLP model training, exporting to `saved_models/` |

---

## 🚀 Quick Start

### 1. Run the Frontend UI
```bash
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

### 2. Run the Backend API (FastAPI)
```bash
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --reload --port 8000
```
- Interactive API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Run Data Cleaning & Model Training
```bash
pip install -r ml/training/requirements.txt
python ml/data_cleaning/clean_resumes.py
python ml/training/train.py
```

---

## 🔄 Integration Workflow

1. **Data Cleaning Team** places raw datasets in `ml/data_cleaning/raw/` and runs `clean_resumes.py` to produce clean data in `ml/data_cleaning/processed/`.
2. **Model Training Team** trains models using data from `ml/data_cleaning/processed/` and exports model weights to `ml/training/saved_models/`.
3. **Backend Team** loads the exported model in `backend/app/services/ml_service.py` and serves REST endpoints (`/api/resumes/upload`, `/api/match`).
4. **Frontend Team** connects the Streamlit dashboard to the backend API endpoints to display real-time inference and rankings.
