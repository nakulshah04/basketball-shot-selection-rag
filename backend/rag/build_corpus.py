import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from backend.config import get_settings

settings = get_settings()

def _value(row: pd.Series, *names: str, default: Any = "unknown") -> Any:
    for name in names:
        value = row.get(name)
        if pd.notna(value):
            return value
    return default


def row_to_document(row: pd.Series, source: str) -> dict[str, Any]:
    """Handle both the synthetic fixture and the NBA shot-chart export schema."""
    player = str(_value(row, "PLAYER_NAME", "player"))
    shot_type = str(_value(row, "SHOT_TYPE", "shot_type"))
    location = str(_value(row, "SHOT_ZONE_BASIC", "location"))
    shot_clock = _value(row, "time_remaining", default="unknown")
    made = _value(row, "SHOT_MADE_FLAG", "shot_success", default=False)
    made = bool(int(made)) if isinstance(made, (int, float)) else str(made).lower() == "true"
    distance = _value(row, "SHOT_DISTANCE", "defender_distance", default="unknown")
    game_date = str(_value(row, "GAME_DATE", default="unknown"))
    event_id = str(_value(row, "GAME_EVENT_ID", default=row.name))
    metadata = {
        "source": source, "source_id": event_id, "player": player,
        "shot_type": shot_type, "location": location, "shot_clock": str(shot_clock),
        "shot_distance": str(distance), "game_date": game_date, "made": made,
    }
    text = (
        f"Source: {source}. Player {player} attempted a {shot_type} from {location} "
        f"with {shot_clock} seconds remaining and shot distance {distance}. "
        f"The shot was {'made' if made else 'missed'} (record {event_id})."
    )
    return {"page_content": text, "metadata": metadata}

def build_corpus(input_path: Path, output_path: Path, source: str) -> int:
    dataframe = pd.read_csv(input_path)
    records = [row_to_document(row, source) for _, row in dataframe.iterrows()]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")
    return len(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=settings.shot_data_csv)
    parser.add_argument("--output", type=Path, default=settings.shot_corpus_jsonl)
    parser.add_argument("--source", default="synthetic development fixture")
    args = parser.parse_args()
    count = build_corpus(args.input, args.output, args.source)
    print(f"Created {count:,} corpus records at {args.output}")

if __name__ == "__main__":
    main()
