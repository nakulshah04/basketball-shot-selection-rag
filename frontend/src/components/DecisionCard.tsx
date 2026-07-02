import type { Decision, Critique } from "../types";

export default function DecisionCard({
  decision,
  critique,
}: {
  decision?: Decision;
  critique?: Critique;
}) {
  return (
    <section className="panel decision-panel">
      <div className="panel-header">
        <h2>Agent Decision</h2>
        {critique && (
          <span className={critique.valid ? "chip success" : "chip danger"}>
            {critique.valid ? "Validated" : "Rejected"}
          </span>
        )}
      </div>

      {!decision ? (
        <p className="muted">Waiting for the first decision...</p>
      ) : (
        <>
          <div className="decision-main">
            <strong>{decision.shot}</strong>
            <span>{Math.round(decision.confidence * 100)}% confidence</span>
          </div>
          <p>{decision.explanation || "No explanation returned."}</p>
        </>
      )}

      {critique && (
        <p className="critique">{critique.reason || "No critique reason returned."}</p>
      )}
    </section>
  );
}
