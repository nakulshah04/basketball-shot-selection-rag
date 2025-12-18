from backend.agents.decision_graph import run_agent
from backend.evaluation.eval_cases import EVAL_QUERIES
from backend.evaluation.utils import safe_json_parse
from backend.evaluation.metrics import compute_metrics

def run():
    results = []

    for q in EVAL_QUERIES:
        output = run_agent(q)

        decision = safe_json_parse(output.get("decision"))
        critique = safe_json_parse(output.get("critique"))

        results.append({
            "query": q,
            "decision": decision.get("shot"),
            "confidence": decision.get("confidence"),
            "valid": critique.get("valid", False),
            "reason": critique.get("reason", "")
        })

    return results

if __name__ == "__main__":
    results = run()

    for r in results:
        print("\nQUERY:", r["query"])
        print("VALID:", r["valid"])
        print("REASON:", r["reason"])

    metrics = compute_metrics(results)
    print("\nMETRICS:")
    for k, v in metrics.items():
        print(f"{k}: {v}")