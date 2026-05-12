class Resume:
    def __init__(self, name: str, raw_skills: str):
        self.name = name
        self.raw_skills = raw_skills
        self.normalized_skills = []
        self.vector = []
