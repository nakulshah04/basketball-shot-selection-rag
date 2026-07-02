import type { GameEvent } from "../types";

export default function EventCard({ event }: { event: GameEvent }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Live Game State</h2>
        <span className="chip">{event.location}</span>
      </div>
      <div className="stat-grid">
        <div>
          <span>Shot Clock</span>
          <strong>{event.time_remaining}s</strong>
        </div>
        <div>
          <span>Score Diff</span>
          <strong>
            {event.score_diff > 0 ? `+${event.score_diff}` : event.score_diff}
          </strong>
        </div>
        <div>
          <span>Defender</span>
          <strong>{event.defender_distance}m</strong>
        </div>
      </div>
    </section>
  );
}
