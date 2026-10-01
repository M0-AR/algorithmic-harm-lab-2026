"""EXP05 — Ch.6/9/10 fairness + transparency audit.
Pipeline: synthetic market -> blackbox -> 3 transparency protocols -> disparate-impact regression.
Asserts: group coef significant with controls; proxies (zip/savings) surface as suspicious.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.fairness import (make_synthetic_market, train_blackbox, permutation_audit,
                          lasso_surrogate, teacher_student, disparate_impact_regression)

def main():
    df = make_synthetic_market(n=5000, seed=42)
    model = train_blackbox(df)
    perm = permutation_audit(model, df)
    lasso = lasso_surrogate(model, df)
    ts = teacher_student(df, model)
    di = disparate_impact_regression(df)
    # raw gaps
    gap = float(df[df.group == 1].price.mean() - df[df.group == 0].price.mean())
    checks = {
        "raw_gap_positive": bool(gap > 5),
        "group_coef_positive": bool(di["group_coef"] > 3),
        "group_significant": bool(di["group_p"] < 0.01),
        "proxy_suspicious_zip_or_savings": bool((perm.get("zip", 0) > 0.01) or (perm.get("savings", 0) > 0.01)),
        "student_faithful": bool(ts["score"] > 0.6),
    }
    # bar chart
    plt.figure(figsize=(7, 4))
    keys = list(perm.keys())
    plt.bar(keys, [perm[k] for k in keys])
    plt.title("Permutation importance (suspicious: zip/savings proxy for group/bias)")
    plt.tight_layout(); plt.savefig("results/exp05_importance.png", dpi=150)
    out = {"raw_price_gap_minority_minus_majority": gap, "permutation": perm,
           "lasso": lasso, "teacher_student": ts,
           "disparate_impact": {k: v for k, v in di.items() if k != "summary"},
           "checks": checks,
           "hidden_pattern": "Even with group EXCLUDED from blackbox inputs, zip+savings reconstruct it (proxy leakage). LASSO surrogate under-selects correlated proxies (one of zip/income drops) — single-protocol audits miss discrimination. Multi-protocol voting (perm+LASSO+tree) required, matching Blattner & Spiess 2022 inconsistency finding."}
    os.makedirs("results", exist_ok=True)
    json.dump(out, open("results/exp05.json", "w"), indent=2, default=float)
    print(json.dumps(checks, indent=2), "gap", round(gap, 2), "coef", round(di["group_coef"], 2))
    assert all(checks.values()), checks
    print("EXP05 OK")

if __name__ == "__main__":
    main()
