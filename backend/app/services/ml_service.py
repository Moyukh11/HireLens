"""
Machine Learning Inference Service
Assigned to: Backend Team (ML Integration)

Responsible for:
- Loading the trained model exported by Teammate 4 from ml/training/saved_models/
- Preprocessing candidate and job description data for the model
- Running inference (e.g. Cosine Similarity, embeddings, classification)
- Returning scores and explainable breakdown
"""

class MLInferenceService:
    def __init__(self):
        # TODO: Load model weights from ml/training/saved_models/
        self.model = None

    def compute_match(self, candidate_data, job_description_data):
        # TODO: Run model inference to compute real match score and breakdown
        raise NotImplementedError("ML inference logic to be implemented by Backend Team")

ml_service = MLInferenceService()
