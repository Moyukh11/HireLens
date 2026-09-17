# Frontend — HireLens UI

**Assigned to:** Frontend Developer  
**Tech Stack:** Streamlit, Python, HTML/CSS  

---

## Getting Started

### 1. Install Dependencies
From the repository root or inside `frontend/`:
```bash
pip install -r frontend/requirements.txt
```

### 2. Run the App
```bash
streamlit run frontend/app.py
```
Or from inside the `frontend/` directory:
```bash
cd frontend
streamlit run app.py
```

---

## Current Status & Temporary Mocks
The files currently in this folder:
- `app.py`: Streamlit application layout, tabs, sessions, and rendering.
- `job_analyzer.py`: *(Mock)* Heuristic skill detection on job descriptions.
- `resume_parser.py`: *(Mock)* PDF/DOCX text extraction and rule-based parsing.
- `scoring.py`: *(Mock)* Formula-based candidate scoring.

> [!NOTE]
> `job_analyzer.py`, `resume_parser.py`, and `scoring.py` are temporary client-side mocks. As the backend and ML teams build real API endpoints, you will replace these local function calls with HTTP calls (`requests.post`) to the FastAPI backend at `http://localhost:8000`.

---

## Upcoming Frontend Tasks
1. **API Integration:**
   - Call `POST http://localhost:8000/api/resumes/upload` when resumes are uploaded.
   - Call `POST http://localhost:8000/api/jobs/analyze` when job description is pasted.
   - Call `POST http://localhost:8000/api/match` to fetch model-driven ranking and confidence scores.
2. **UI Enhancements:**
   - Add loading spinners / progress bars for batch resume processing.
   - Add candidate comparison view and filters (by score threshold, missing skills).
   - Display real ML model explainability data (e.g. semantic match score vs hard skill match).
