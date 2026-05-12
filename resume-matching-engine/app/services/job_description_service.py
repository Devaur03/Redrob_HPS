import csv
from app.models.job_description import JobDescription

class JobDescriptionService:
    def __init__(self, skill_aliases: dict):
        self.skill_aliases = skill_aliases

    def load_job_descriptions(self, filepath: str) -> list[JobDescription]:
        jds = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jds.append(JobDescription(row['Name'], row['Skills']))
        return jds

    def normalize_skills(self, raw_skills: str) -> list[str]:
        if not raw_skills:
            return []
        
        result = []
        for token in raw_skills.split(","):
            key = token.strip().lower()
            if key in self.skill_aliases:
                result.append(self.skill_aliases[key])
                
        return list(set(result))

    def build_binary_vector(self, skills: list[str], vocabulary: list[str]) -> list[int]:
        skill_set = set(skills)
        return [1 if term in skill_set else 0 for term in vocabulary]

    def process_job_descriptions(self, jds: list[JobDescription], vocabulary: list[str]):
        for jd in jds:
            jd.normalized_skills = self.normalize_skills(jd.raw_skills)
            jd.vector = self.build_binary_vector(jd.normalized_skills, vocabulary)
