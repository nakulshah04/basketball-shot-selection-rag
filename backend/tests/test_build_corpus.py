import pandas as pd

from backend.rag.build_corpus import row_to_document


def test_row_to_document_preserves_nba_source_and_metadata():
    record = row_to_document(
        pd.Series({
            "PLAYER_NAME": "A Player", "SHOT_TYPE": "3PT Field Goal",
            "SHOT_ZONE_BASIC": "Above the Break 3", "SHOT_MADE_FLAG": 1,
            "SHOT_DISTANCE": 26, "GAME_DATE": "20250101", "GAME_EVENT_ID": 7,
        }),
        "NBA Stats shot chart detail, 2024-25 regular season",
    )
    assert record["metadata"]["source_id"] == "7"
    assert record["metadata"]["made"] is True
    assert "Source: NBA Stats" in record["page_content"]
