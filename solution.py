import math

DEBUG = False

# SKILL_ALIASES derived from the constraints and examples provided
SKILL_ALIASES = {
    "pyhton": "python",
    "python": "python",
    "javascrpit": "javascript",
    "javascript": "javascript",
    "vue.js": "vue",
    "vue": "vue",
    "machine learning": "machine_learning",
    "machine_learning": "machine_learning",
    "deep-learning": "deep_learning",
    "deep learning": "deep_learning",
    "deep_learning": "deep_learning",
    "matplotlib": "data_visualization",
    "data_visualization": "data_visualization",
    "sql": "sql",
    "pandas": "pandas",
    "numpy": "numpy",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch"
}

def normalize_skills(raw_skill_string):
    """
    Converts noisy comma-separated skill string into deduplicated canonical skills.
    Tokens are split by comma, stripped, lowercased, and mapped using SKILL_ALIASES.
    Unknown skills are discarded.
    """
    if not raw_skill_string:
        return []
    
    result = []
    for token in raw_skill_string.split(","):
        key = token.strip().lower()
        if key in SKILL_ALIASES:
            result.append(SKILL_ALIASES[key])
            
    # Deduplicate canonical skills per resume (using set, then back to list)
    return list(set(result))

def build_vocabulary(normalized_resumes):
    """
    Builds sorted global vocabulary from all processed resumes.
    """
    vocab_set = set()
    for resume in normalized_resumes:
        vocab_set.update(resume)
    return sorted(list(vocab_set))

def compute_document_frequency(normalized_resumes, vocabulary):
    """
    Computes the number of documents (resumes) each skill appears in.
    """
    df = {term: 0 for term in vocabulary}
    for resume in normalized_resumes:
        skill_set = set(resume)
        for term in vocabulary:
            if term in skill_set:
                df[term] += 1
    return df

def compute_tfidf_vectors(normalized_resumes, vocabulary, df):
    """
    Builds continuous TF-IDF vector for all resumes.
    TF = 1 / N (where N is the number of unique normalized skills)
    IDF = ln(10 / df) (unsmoothed)
    """
    total_docs = len(normalized_resumes)
    
    # Precompute IDF map
    idf_map = {}
    for term in vocabulary:
        # If term is in vocab, df[term] is guaranteed to be >= 1
        idf_map[term] = math.log(total_docs / df[term])
        
    vectors = []
    for resume in normalized_resumes:
        skill_set = set(resume)
        n_skills = len(skill_set)
        
        vec = []
        if n_skills == 0:
            # Empty Resume After Normalization
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

def build_binary_vector(skills, vocabulary):
    """
    Builds binary vector for a JD.
    1 if JD contains the skill, 0 otherwise.
    """
    skill_set = set(skills)
    return [1 if term in skill_set else 0 for term in vocabulary]

def cosine_similarity(vec1, vec2):
    """
    Computes cosine similarity manually safely, avoiding division by zero.
    """
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag_a = math.sqrt(sum(a * a for a in vec1))
    mag_b = math.sqrt(sum(b * b for b in vec2))

    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    return dot / (mag_a * mag_b)

def rank_candidates(jd, resumes, resume_vectors, vocabulary):
    """
    Ranks all candidates for one JD and returns top 3.
    """
    jd_skills = normalize_skills(jd["skills"])
    jd_vector = build_binary_vector(jd_skills, vocabulary)
    
    if DEBUG:
        print(f"\n--- Debug JD: {jd['name']} ---")
        print(f"JD Vector: {jd_vector}")
    
    scores = []
    for i, candidate in enumerate(resumes):
        score = cosine_similarity(resume_vectors[i], jd_vector)
        # Round internal score to around 5 decimals before sorting to avoid floating-point tie errors
        scores.append((candidate["name"], round(score, 5)))
        
    # Sort by descending score, ascending candidate name
    scores.sort(key=lambda x: (-x[1], x[0]))
    
    if DEBUG:
        for name, score in scores:
            print(f"  {name}: {score}")
            
    # Return top 3 candidates
    return scores[:3]

def main():
    # 1. Raw Candidate and JD Data
    # Used 10 resumes and 3 JDs to match the total doc count (10) for IDF scaling
    resumes = [
        {"name": "Alice Smith", "skills": "Pyhton, Machine Learning, SQL, pandas, numpy, Deep-learning"},
        {"name": "Bob Jones", "skills": "javascrpit, vue.js, unknown_skill"},
        {"name": "Charlie Brown", "skills": "Python, SQL"},
        {"name": "Diana Prince", "skills": "matplotlib, pandas, numpy"},
        {"name": "Eve Adams", "skills": "machine learning, deep-learning, pyhton"},
        {"name": "Frank White", "skills": "sql, python"},
        {"name": "Grace Lee", "skills": "Machine Learning, Deep Learning, TensorFlow, PyTorch, Pyhton"},
        {"name": "Henry Ford", "skills": "javascript, vue"},
        {"name": "Ivy Chen", "skills": "SQL, pandas"},
        {"name": "Jack Wilson", "skills": "unknown_skill1, unknown_skill2"} # Edge case: all unknown
    ]

    jds = [
        {"name": "Data Scientist", "skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization"},
        {"name": "Frontend Developer", "skills": "javascript, vue, react"},
        {"name": "Data Analyst", "skills": "Python, SQL, pandas, numpy, matplotlib"}
    ]

    # 2. Normalize all resumes
    normalized_resumes = [normalize_skills(r["skills"]) for r in resumes]
    
    if DEBUG:
        print("--- Normalized Resumes ---")
        for i, r in enumerate(resumes):
            print(f"{r['name']}: {normalized_resumes[i]}")

    # 3. Build global vocabulary
    vocabulary = build_vocabulary(normalized_resumes)
    
    if DEBUG:
        print(f"\n--- Vocabulary (Size: {len(vocabulary)}) ---")
        print(vocabulary)

    # 4. Compute Document Frequency
    df = compute_document_frequency(normalized_resumes, vocabulary)
    
    if DEBUG:
        print("\n--- Document Frequency ---")
        print(df)

    # 5. Compute TF-IDF Vectors
    resume_vectors = compute_tfidf_vectors(normalized_resumes, vocabulary, df)
    
    if DEBUG:
        print("\n--- Resume TF-IDF Vectors ---")
        for i, vec in enumerate(resume_vectors):
            print(f"{resumes[i]['name']}: {vec}")

    # 6. Rank Candidates per JD and Print Format
    for jd in jds:
        print(f"{jd['name']}:")
        top_3 = rank_candidates(jd, resumes, resume_vectors, vocabulary)
        for name, score in top_3:
            # Round scores to 2 decimals for display
            print(f"{name} ({score:.2f})")
        print() # Empty line separation

if __name__ == "__main__":
    main()
