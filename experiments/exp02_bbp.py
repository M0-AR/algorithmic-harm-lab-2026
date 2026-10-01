"""EXP02 — Ch.2 BBP exact replication (Tables 2.1/2.2) + correlated-misperception sweep."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from src.bbp import bbp_U, bbp_S, bbp_baseline

def main(V=100.0):
    base = bbp_baseline(V)
    u = bbp_U(V); s = bbp_S(V)
    checks = {
        "U_profit_up": u.profit > base["profit"],           # 28/49 V > 1/2 V
        "U_cs_down": u.cs < base["cs"],                     # 11/49 < 1/4
        "S_profit_down": s.profit < base["profit"],         # 0.45 < 0.5
        "S_cs_up": s.cs > base["cs"],                       # 0.325 > 0.25
        "U_numbers": abs(u.profit - 28/49*V) < 1e-9 and abs(u.cs - 11/49*V) < 1e-9,
        "S_numbers": abs(s.profit - 0.45*V) < 1e-9 and abs(s.cs - 0.325*V) < 1e-9,
    }
    # sweep: strategic awareness share -> aggregate CS interpolates U->S
    shares = np.linspace(0, 1, 11)  # share strategic
    agg = [(1-x)*u.cs + x*s.cs for x in shares]
    plt.figure(figsize=(6, 4))
    plt.plot(shares, agg, marker="o")
    plt.axhline(base["cs"], color="gray", linestyle="--", label="No-BBP CS=25")
    plt.xlabel("Share strategic (S)"); plt.ylabel("Aggregate consumer surplus")
    plt.title("BBP: U->S interpolation (hidden pattern: tipping at ~0.3)")
    plt.legend(); plt.tight_layout(); plt.savefig("results/exp02_bbp.png", dpi=150)
    # hidden pattern: find crossover where BBP becomes net-positive vs baseline
    cross = float(shares[next(i for i,v in enumerate(agg) if v > base["cs"])])
    out = {"baseline": base, "U": vars(u), "S": vars(s),
           "checks": checks, "crossover_share_S": cross,
           "hidden_pattern": "BBP aggregate CS is U-harmful but S-beneficial; crossover at S-share≈%.2f. Poor subgroups gain even in U (Table 2.1 rows 2-3), rich lose — distributional flip invisible in aggregates." % cross}
    os.makedirs("results", exist_ok=True)
    json.dump(out, open("results/exp02.json", "w"), indent=2, default=str)
    print(json.dumps(checks, indent=2), "crossover", cross)
    assert all(checks.values())
    print("EXP02 OK")

if __name__ == "__main__":
    main()
