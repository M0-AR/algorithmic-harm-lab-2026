"""EXP01 — Ch.1 baseline: S vs U price discrimination.
Reproduces Figs 1.1-1.4 numerically + imperfect segmentation.
Asserts book theorems: S: CS->0, DWL->0; U-over: CS negative, DWL ambiguous.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from src.demand import MarketParams, monopoly_no_discrimination, perfect_price_discrimination, imperfect_segmentation_surplus

OUT = "results/exp01.json"

def main():
    V, c = 100.0, 10.0
    # S market
    s_no = monopoly_no_discrimination(MarketParams(V, c, 0.0))
    s_pd = perfect_price_discrimination(MarketParams(V, c, 0.0))
    # U over
    u_no = monopoly_no_discrimination(MarketParams(V, c, 30.0))
    u_pd = perfect_price_discrimination(MarketParams(V, c, 30.0))
    # U under
    uu_no = monopoly_no_discrimination(MarketParams(V, c, -20.0))
    uu_pd = perfect_price_discrimination(MarketParams(V, c, -20.0))
    # imperfect
    imp_s = imperfect_segmentation_surplus(V, c, 0.0, 4)
    imp_u = imperfect_segmentation_surplus(V, c, 30.0, 4)
    res = {
        "S_no": s_no, "S_pd": s_pd,
        "Uover_no": u_no, "Uover_pd": u_pd,
        "Uunder_no": uu_no, "Uunder_pd": uu_pd,
        "imperfect_S4": imp_s, "imperfect_U4": imp_u,
        "theorem_checks": {
            "S_CS_erased": bool(abs(s_pd["cs"]) < 1e-9),
            "S_DWL_eliminated": bool(abs(s_pd["dwl"]) < 1e-9),
            "S_profit_up": bool(s_pd["profit"] > s_no["profit"]),
            "Uover_CS_negative": bool(u_pd["cs"] < 0),
            "Uover_CS_worse_than_S": bool(u_pd["cs"] < s_pd["cs"]),
            "Uover_profit_highest": bool(u_pd["profit"] > s_pd["profit"]),
            "Uunder_efficiency_up": bool(uu_pd["dwl"] < uu_no["dwl"]),
            "imperfect_S_leaves_CS": bool(imp_s["cs"] > 0),
        }
    }
    os.makedirs("results", exist_ok=True)
    # sanitize numpy types
    def _py(o):
        import numpy as _np
        if isinstance(o, dict):
            return {k: _py(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_py(v) for v in o]
        if isinstance(o, (_np.generic,)):
            return o.item()
        return o
    res = _py(res)
    json.dump(res, open(OUT, "w"), indent=2)
    # figure: demand curves
    q = np.linspace(0, 1, 200)
    p_true = V - V * q
    p_perc = V + 30 - V * q
    plt.figure(figsize=(7, 4.5))
    plt.plot(q, p_true, label="Actual demand")
    plt.plot(q, p_perc, "--", label="Perceived demand (overest.)")
    plt.axhline(c, color="gray", label=f"Supply c={c}")
    plt.scatter([s_no["qm"]], [s_no["pm"]], c="black", zorder=5, label=f"S monopoly")
    plt.scatter([u_no["qm"]], [u_no["pm"]], c="red", zorder=5, label="U monopoly")
    plt.xlabel("Quantity"); plt.ylabel("Price"); plt.legend(); plt.tight_layout()
    plt.savefig("results/exp01_demand.png", dpi=150)
    print(json.dumps(res["theorem_checks"], indent=2))
    assert all(res["theorem_checks"].values()), "theorem check failed"
    print("EXP01 OK ->", OUT)

if __name__ == "__main__":
    main()
