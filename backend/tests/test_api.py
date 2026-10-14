from fastapi.testclient import TestClient

from backend import app as app_module


def test_decision_endpoint_returns_structured_evidence(monkeypatch):
    monkeypatch.setattr(app_module, "run_agent", lambda query: {
        "decision": {"shot": "3PT", "explanation": "Open look.", "confidence": 0.8},
        "critique": {"valid": True, "reason": "Grounded."},
        "evidence": [{
            "source": "NBA Stats", "source_id": "1", "player": "A Player",
            "location": "Left Corner 3", "shot_type": "3PT Field Goal",
            "made": True, "text": "Recorded shot.",
        }],
    })
    response = TestClient(app_module.app).post("/api/decisions", json={
        "time_remaining": 8, "score_diff": -2,
        "defender_distance": 3.0, "location": "left wing",
    })
    assert response.status_code == 200
    assert response.json()["evidence"][0]["source_id"] == "1"
