"""
Resume Parser Service
Assigned to: Backend Team

Responsible for:
- Reading uploaded files (PDF / DOCX / TXT)
- Extracting raw text and sections (Experience, Education, Skills, Projects)
- Parsing contact info and structured candidate data
"""

class ResumeParserService:
    @staticmethod
    def extract_text(file_bytes: bytes, filename: str) -> str:
        # TODO: Implement text extraction for PDF, DOCX, TXT
        raise NotImplementedError("Text extraction to be implemented by Backend Team")

    @staticmethod
    def parse_candidate(text: str, filename: str, candidate_id: str):
        # TODO: Implement candidate parsing (Regex, spaCy NER, or LLM)
        raise NotImplementedError("Candidate parsing to be implemented by Backend Team")
