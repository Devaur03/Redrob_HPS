from app.utils.cosine_similarity_calculator import CosineSimilarityCalculator
from app.models.resume import Resume
from app.models.job_description import JobDescription

class MatchingService:
    @staticmethod
    def rank_candidates(jd: JobDescription, resumes: list[Resume]) -> list[tuple[str, float]]:
        scores = []
        for r in resumes:
            score = CosineSimilarityCalculator.compute(r.vector, jd.vector)
            scores.append((r.name, round(score, 5)))
            
        scores.sort(key=lambda x: (-x[1], x[0]))
        return scores[:3]
