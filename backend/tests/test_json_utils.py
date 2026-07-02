from backend.utils.json_utils import (
    normalize_critique,
    normalize_decision,
    safe_json_parse,
)


def test_safe_json_parse_accepts_fenced_json():
    assert safe_json_parse('```json\n{"valid": true, "reason": "grounded"}\n```') == {
        "valid": True,
        "reason": "grounded",
    }


def test_safe_json_parse_extracts_object_from_text():
    assert safe_json_parse('Decision follows: {"shot": "3PT", "confidence": 0.8}') == {
        "shot": "3PT",
        "confidence": 0.8,
    }


def test_normalize_decision_clamps_confidence_and_defaults_shot():
    decision = normalize_decision('{"confidence": 3, "explanation": "Open look."}')

    assert decision == {
        "shot": "INSUFFICIENT EVIDENCE",
        "explanation": "Open look.",
        "confidence": 1.0,
    }


def test_normalize_critique_handles_string_boolean():
    assert normalize_critique('{"valid": "true", "reason": "Uses retrieved facts."}') == {
        "valid": True,
        "reason": "Uses retrieved facts.",
    }
