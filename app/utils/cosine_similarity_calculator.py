import math

class CosineSimilarityCalculator:
    @staticmethod
    def compute(vec1, vec2):
        dot = sum(a * b for a, b in zip(vec1, vec2))
        mag_a = math.sqrt(sum(a * a for a in vec1))
        mag_b = math.sqrt(sum(b * b for b in vec2))

        if mag_a == 0.0 or mag_b == 0.0:
            return 0.0

        return dot / (mag_a * mag_b)
