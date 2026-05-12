# Resume Matching Engine

A heuristic-based resume matching engine that ranks candidates against job descriptions using TF-IDF and Cosine Similarity. Built strictly with standard Python libraries.

## Architecture

- **Models**: Simple representation of Resumes, JDs, and configuration loading.
- **Services**: Business logic to ingest data, normalize skills, and match vectors.
- **Utils**: Math operations separated into calculators (TF-IDF, Cosine Similarity).
- **Data**: CSV formats for inputs, JSON for alias matching.

## Execution

Ensure you are using Python 3.9+ and run:

```bash
python app/main.py
```

## Constraints Met
- Native Python only (no Pandas, NumPy, Scikit-learn).
- Modular design following MVC/Service patterns.
- Handles empty/unknown skill edge cases safely.
