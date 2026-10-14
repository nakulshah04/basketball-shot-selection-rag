"""Download source-traceable NBA shot-chart data for the retrieval corpus."""

from __future__ import annotations

import argparse
from pathlib import Path


def download_shots(season: str, output_path: Path) -> int:
    """Fetch league-wide regular-season field-goal attempts from NBA Stats."""
    try:
        from nba_api.stats.endpoints import shotchartdetail
    except ImportError as exc:  # pragma: no cover - exercised by the CLI
        raise RuntimeError("Install requirements before downloading NBA data.") from exc

    response = shotchartdetail.ShotChartDetail(
        team_id=0, player_id=0, context_measure_simple="FGA",
        season_nullable=season, season_type_all_star="Regular Season", timeout=30,
    )
    shots = response.get_data_frames()[0]
    if shots.empty:
        raise RuntimeError(f"NBA Stats returned no shot attempts for {season}.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shots.to_csv(output_path, index=False)
    return len(shots)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", default="2024-25")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or Path(f"backend/data/nba_shots_{args.season}.csv")
    print(f"Saved {download_shots(args.season, output):,} NBA shot attempts to {output}")


if __name__ == "__main__":
    main()
