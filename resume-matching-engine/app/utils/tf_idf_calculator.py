import math

class TfIdfCalculator:
    @staticmethod
    def compute_document_frequency(normalized_resumes, vocabulary):
        df = {term: 0 for term in vocabulary}
        for resume in normalized_resumes:
            skill_set = set(resume)
            for term in vocabulary:
                if term in skill_set:
                    df[term] += 1
        return df

    @staticmethod
    def compute_tfidf_vectors(normalized_resumes, vocabulary, df):
        total_docs = len(normalized_resumes)
        idf_map = {}
        for term in vocabulary:
            idf_map[term] = math.log(total_docs / df[term]) if df[term] > 0 else 0.0
            
        vectors = []
        for resume in normalized_resumes:
            skill_set = set(resume)
            n_skills = len(skill_set)
            
            vec = []
            if n_skills == 0:
                vec = [0.0] * len(vocabulary)
            else:
                tf = 1.0 / n_skills
                for term in vocabulary:
                    if term in skill_set:
                        vec.append(tf * idf_map[term])
                    else:
                        vec.append(0.0)
            vectors.append(vec)
            
        return vectors
