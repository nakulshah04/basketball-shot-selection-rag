import random
import pandas as pd

PLAYERS = ["Player A", "Player B", "Player C"]
SHOT_TYPES = ["LAYUP", "MIDRANGE", "3PT"]
LOCATIONS = ["paint", "left wing", "right wing", "top of key"]

def generate_row():
    shot_type = random.choices(
        SHOT_TYPES, weights=[0.35, 0.30, 0.35]
    )[0]

    return {
        "player": random.choice(PLAYERS),
        "shot_type": shot_type,
        "location": random.choice(LOCATIONS),
        "defender_distance": round(random.uniform(0.5, 4.0), 2),
        "time_remaining": random.randint(1, 24),
        "score_diff": random.randint(-10, 10),
        "shot_success": random.random() < {
            "LAYUP": 0.65,
            "MIDRANGE": 0.45,
            "3PT": 0.38
        }[shot_type]
    }

def main(n=5000):
    data = [generate_row() for _ in range(n)]
    df = pd.DataFrame(data)
    df.to_csv("backend/data/shot_data.csv", index=False)
    print(f"Generated {n} rows")

if __name__ == "__main__":
    main()