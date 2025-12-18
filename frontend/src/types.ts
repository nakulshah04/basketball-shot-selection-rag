export interface GameEvent {
  time_remaining: number;
  score_diff: number;
  defender_distance: number;
  location: string;
}

export interface Decision {
  shot: string;
  explanation: string;
  confidence: number;
}

export interface Critique {
  valid: boolean;
  reason: string;
}

export interface StreamPayload {
  status?: string;
  event?: GameEvent;
  decision?: Decision | string;
  critique?: Critique | string;
}