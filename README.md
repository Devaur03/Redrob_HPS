# Resume Matching Engine

A heuristic-based resume matching engine that ranks candidates against job descriptions using TF-IDF and Cosine Similarity. Built strictly with standard Python libraries.

## Architecture & Folder Structure

This project follows a modular, production-ready backend architecture separating data, configuration, business logic, and mathematical operations.

```text
├── app/
│   ├── models/       # Simple data classes representing Resumes, Job Descriptions, and Skill Aliases
│   ├── services/     # Core business logic (Normalization, Vector Processing, Matching)
│   ├── utils/        # Pure mathematical calculators for TF-IDF and Cosine Similarity
│   └── main.py       # Application entrypoint that orchestrates the pipeline
├── config/           # Centralized application settings and path definitions
├── data/             # CSV files for inputs (Resumes, JDs) and JSON for skill aliases
```

### Logical Pipeline

1. **Normalization & Deduplication**: Raw skill strings are split by commas, stripped, lowercased, and matched against a canonical alias dictionary. Unknown skills are discarded. Skills are deduplicated per resume.
2. **Vocabulary Construction**: A global, alphabetically-sorted vocabulary is built strictly from the canonical skills present in the resume dataset.
3. **TF-IDF Vectorization**: Resumes are vectorized.
   - **Term Frequency (TF)** = `1 / N` (where N is the number of unique canonical skills in that resume) to penalize keyword stuffing.
   - **Inverse Document Frequency (IDF)** = `ln(10 / df)` (unsmoothed natural logarithm) to penalize ubiquitous skills.
4. **Binary JD Vectorization**: Job Descriptions are mapped to the global vocabulary using binary vectors (`1` if required, `0` otherwise).
5. **Cosine Similarity**: Candidates are ranked by computing the cosine similarity between their TF-IDF vector and the JD's binary vector. Ties are broken alphabetically.

## Execution

Ensure you are using Python 3.9+ and run:

```bash
python app/main.py
```

## Constraints Met
- **Native Python only**: No external ML libraries (Pandas, NumPy, Scikit-learn) are used.
- **Robust Edge Cases**: Handles empty resumes, unknown skills, and zero-magnitude vectors securely.
