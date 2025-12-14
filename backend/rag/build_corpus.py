import pandas as pd

INPUT_CSV = "backend/data/shot_data.csv"
OUTPUT_TXT = "backend/rag/shot_corpus.txt"

def row_to_text(row):
    return (
        f"Player {row.player} attempted a {row.shot_type} from the {row.location} "
        f"with defender distance {row.defender_distance} meters, "
        f"{row.time_remaining} seconds on the shot clock, "
        f"score difference {row.score_diff}. "
        f"The shot was {'made' if row.shot_success else 'missed'}."
    )

def main():
    df = pd.read_csv(INPUT_CSV)
    texts = df.apply(row_to_text, axis=1).tolist()

    with open(OUTPUT_TXT, "w") as f:
        for t in texts:
            f.write(t + "\n")

    print(f"Created corpus with {len(texts)} entries")

if __name__ == "__main__":
    main()