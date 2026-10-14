# Data sources

The production retrieval corpus is built from a versioned CSV snapshot obtained
from the NBA's public shot-chart statistics endpoint through `nba_api`.

```bash
python -m backend.data.ingest_nba_shots --season 2024-25
python -m backend.rag.build_corpus --input backend/data/nba_shots_2024-25.csv \
  --source "NBA Stats shot chart detail, 2024-25 regular season"
```

NBA Stats is the first-party source for these recorded field-goal attempts.
Its public endpoint is undocumented and can change or rate-limit requests, so
the application uses downloaded snapshots rather than querying it at runtime.

`shot_data.csv` remains a synthetic development fixture. It must not be
described as historical NBA data in demos, evaluations, or documentation.
