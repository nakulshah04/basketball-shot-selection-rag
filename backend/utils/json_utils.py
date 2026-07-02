import json
import re
from typing import Any


def safe_json_parse(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if not isinstance(value, str):
        return {}

    candidates = [value.strip()]
    fenced_match = re.search(r"```(?:json)?\s*(.*?)```", value, re.DOTALL | re.IGNORECASE)
    if fenced_match:
        candidates.append(fenced_match.group(1).strip())

    object_match = re.search(r"\{.*\}", value, re.DOTALL)
    if object_match:
        candidates.append(object_match.group(0))

    for candidate in candidates:
        if not candidate:
            continue
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed

    return {}


def normalize_decision(value: Any) -> dict[str, Any]:
    parsed = safe_json_parse(value)
    shot = str(parsed.get("shot", "INSUFFICIENT EVIDENCE")).upper()
    confidence = parsed.get("confidence", 0.0)
    try:
        confidence = max(0.0, min(1.0, float(confidence)))
    except (TypeError, ValueError):
        confidence = 0.0

    return {
        "shot": shot,
        "explanation": str(parsed.get("explanation", "")).strip(),
        "confidence": confidence,
    }


def normalize_critique(value: Any) -> dict[str, Any]:
    parsed = safe_json_parse(value)
    valid = parsed.get("valid", False)
    if isinstance(valid, str):
        valid = valid.strip().lower() == "true"

    return {
        "valid": bool(valid),
        "reason": str(parsed.get("reason", "")).strip(),
    }
