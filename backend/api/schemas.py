from typing import Literal

from pydantic import BaseModel, Field


class GameSituation(BaseModel):
    time_remaining: int = Field(ge=0, le=48 * 60)
    score_diff: int = Field(ge=-100, le=100)
    defender_distance: float = Field(ge=0, le=20)
    location: str = Field(min_length=1, max_length=80)

    def to_query(self) -> str:
        return (
            f"{self.time_remaining} seconds left, score difference {self.score_diff}, "
            f"defender {self.defender_distance} meters away at {self.location}"
        )


class Evidence(BaseModel):
    source: str
    source_id: str
    player: str
    location: str
    shot_type: str
    made: bool
    text: str


class Decision(BaseModel):
    shot: str
    explanation: str
    confidence: float = Field(ge=0, le=1)


class Critique(BaseModel):
    valid: bool
    reason: str


class DecisionResponse(BaseModel):
    situation: GameSituation
    decision: Decision
    critique: Critique
    evidence: list[Evidence]
