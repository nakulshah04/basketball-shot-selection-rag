import type { GameEvent } from "../types";

export default function EventCard({ event }: { event: GameEvent }) {
  return (
    <div style={{ border: "1px solid #ccc", padding: 12 }}>
      <h3>Live Game State</h3>
      <p>Time left: {event.time_remaining}s</p>
      <p>Score diff: {event.score_diff}</p>
      <p>Defender distance: {event.defender_distance}m</p>
      <p>Location: {event.location}</p>
    </div>
  );
}