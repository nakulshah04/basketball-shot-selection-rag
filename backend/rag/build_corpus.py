import pandas as pd

from backend.config import get_settings

settings = get_settings()

def row_to_text(row):
    return (
        f"Player {row.player} attempted a {row.shot_type} from the {row.location} "
        f"with defender distance {row.defender_distance} meters, "
        f"{row.time_remaining} seconds on the shot clock, "
        f"score difference {row.score_diff}. "
        f"The shot was {'made' if row.shot_success else 'missed'}."
    )

def main():
    df = pd.read_csv(settings.shot_data_csv)
    texts = df.apply(row_to_text, axis=1).tolist()

    with open(settings.shot_corpus_txt, "w") as f:
        for t in texts:
            f.write(t + "\n")

    print(f"Created corpus with {len(texts)} entries")

if __name__ == "__main__":
    main()
