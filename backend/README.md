# Backend — HireLens API & Services

**Assigned to:** Member 2 & Member 3  
**Tech Stack:** FastAPI, Pydantic, Uvicorn, SQLite/SQLAlchemy  

---

## Getting Started

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Run the Backend Server
From inside the `backend` folder:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
API Documentation (Interactive Swagger UI) will be live at:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Role Division (Member 2 & Member 3)

### Member 2: API & Data Persistence
- [ ] **Database Setup:** Add SQLite with SQLAlchemy or Tortoise ORM (`app/database.py`).
- [ ] **Data Persistence:** Store uploaded candidates, job descriptions, and previous scoring runs so refreshing the page doesn't wipe history.
- [ ] **Candidate Management Endpoints:**
  - `GET /api/candidates`: Retrieve all saved candidates.
  - `DELETE /api/candidates/{id}`: Delete a candidate.
- [ ] **CORS & Error Handling:** Ensure smooth communication with the Streamlit frontend.

### Member 3: Parsing & ML Integration Service
- [ ] **Resume Parsing Pipeline (`app/services/parser_service.py`):**
  - Extract sections: Work Experience, Education, Technical Skills, Projects.
  - Integrate a skill dictionary or spaCy NER pipeline for automated skill tagging.
- [ ] **Model Serving (`app/services/ml_service.py`):**
  - Coordinate with Member 6 (Model Trainer) to load the trained model weights from `ml/training/saved_models/`.
  - Implement vector/embedding similarity (e.g. Sentence-BERT or TF-IDF cosine similarity) to calculate real semantic match scores.
  - Generate explainable breakdowns for the frontend (which skills matched, why candidate is strong/weak).

---

## API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check endpoint |
| `POST` | `/api/resumes/upload` | Upload multiple PDF/DOCX resumes and parse text |
| `POST` | `/api/jobs/analyze` | Parse job description text into structured criteria |
| `POST` | `/api/match` | Run ML matching and return ranked candidate scores |
