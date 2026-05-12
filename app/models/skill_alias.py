import json

class SkillAliasLoader:
    @staticmethod
    def load_aliases(filepath: str) -> dict:
        with open(filepath, 'r') as f:
            return json.load(f)
