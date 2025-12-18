import type { Decision, Critique } from "../types";

export default function DecisionCard({
  decision,
  critique,
}: {
  decision?: Decision;
  critique?: Critique;
}) {
  if (!decision) return null;

  return (
    <div style={{ border: "1px solid #ccc", padding: 12 }}>
      <h3>Agent Decision</h3>
      <p><b>Shot:</b> {decision.shot}</p>
      <p><b>Confidence:</b> {decision.confidence}</p>
      <p>{decision.explanation}</p>

      {critique && (
        <p style={{ color: critique.valid ? "green" : "red" }}>
          {critique.valid ? "✔ Validated" : "✖ Rejected"} — {critique.reason}
        </p>
      )}
    </div>
  );
}