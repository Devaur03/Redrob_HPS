import csv
from app.models.resume import Resume
from app.utils.tf_idf_calculator import TfIdfCalculator

class ResumeService:
    def __init__(self, skill_aliases: dict):
        self.skill_aliases = skill_aliases

    def load_resumes(self, filepath: str) -> list[Resume]:
        resumes = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                resumes.append(Resume(row['Name'], row['Skills']))
        return resumes

    def normalize_skills(self, raw_skills: str) -> list[str]:
        if not raw_skills:
            return []
        
        result = []
        for token in raw_skills.split(","):
            key = token.strip().lower()
            if key in self.skill_aliases:
                result.append(self.skill_aliases[key])
                
        return list(set(result))

    def build_vocabulary(self, resumes: list[Resume]) -> list[str]:
        vocab_set = set()
        for r in resumes:
            vocab_set.update(r.normalized_skills)
        return sorted(list(vocab_set))

    def process_resumes(self, resumes: list[Resume]) -> tuple[list[str], dict]:
        for r in resumes:
            r.normalized_skills = self.normalize_skills(r.raw_skills)
            
        vocabulary = self.build_vocabulary(resumes)
        normalized_lists = [r.normalized_skills for r in resumes]
        df = TfIdfCalculator.compute_document_frequency(normalized_lists, vocabulary)
        vectors = TfIdfCalculator.compute_tfidf_vectors(normalized_lists, vocabulary, df)
        
        for i, r in enumerate(resumes):
            r.vector = vectors[i]
            
        return vocabulary, df
