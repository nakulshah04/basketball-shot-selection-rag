import type { Evidence } from "../types";

export default function EvidenceCard({ evidence }: { evidence: Evidence[] }) {
  return (
    <section className="panel evidence-panel">
      <div className="panel-header">
        <div>
          <p className="section-kicker">Retrieval trail</p>
          <h2>Comparable shot attempts</h2>
        </div>
        <span className="chip">{evidence.length} records</span>
      </div>
      {evidence.length === 0 ? (
        <p className="muted">Waiting for source-backed examples...</p>
      ) : (
        <ol className="evidence-list">
          {evidence.slice(0, 3).map((item) => (
            <li key={`${item.source}-${item.source_id}`}>
              <div>
                <strong>{item.player}</strong>
                <span>{item.shot_type} · {item.location}</span>
              </div>
              <span className={item.made ? "result made" : "result missed"}>
                {item.made ? "made" : "missed"}
              </span>
            </li>
          ))}
        </ol>
      )}
      <p className="source-note">Each record stays linked to its source ID so the recommendation can be audited.</p>
    </section>
  );
}
