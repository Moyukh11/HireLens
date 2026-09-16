# HireLens — Resume Screener & Job Matcher

HireLens is a Streamlit application for parsing resumes, analyzing job descriptions, and ranking candidates with explainable scores. It is a self-contained local app; it does not use a separate backend server, database, or external AI service.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser.

## Workflow

1. Upload PDF, DOCX, or TXT resumes, or paste resume text.
2. Paste a job description and select **Detect skills**.
3. Open the **Dashboard** to review the ranked candidate list.

The sidebar provides navigation between all three sections. The Dashboard can also be opened before the previous steps are complete and will show an empty state.

## Features
- Upload multiple PDF, DOCX, or TXT resumes
- Paste resume text directly
- Extract name, email, phone, skills, education, and experience
- Paste a job description
- Detect required/preferred skills and experience/degree requirements
- Explainable 0–100 matching score using 70% skills / 20% experience / 10% education
- Ranked candidate cards with matched/missing skills

## Project Structure

```text
app.py             Streamlit UI, navigation, session state, and dashboard
resume_parser.py   PDF/DOCX/TXT extraction and resume parsing
job_analyzer.py    Job-description skill and requirement detection
scoring.py         Explainable candidate scoring
requirements.txt   Python dependencies
```

## Processing Model

Resume parsing, job-description analysis, and candidate scoring run locally in the Streamlit process. Uploaded content is not sent to an external AI service.
