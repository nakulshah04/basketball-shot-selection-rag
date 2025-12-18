def compute_metrics(results):
    total = len(results)
    valid = sum(1 for r in results if r["valid"])
    rejected = total - valid

    return {
        "total_cases": total,
        "valid_decisions": valid,
        "rejected_decisions": rejected,
        "rejection_rate": rejected / total if total > 0 else 0.0
    }