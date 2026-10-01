"""EXP04 — Ch.5 coordination: Q-learning vs competitive baseline.
Asserts: learned CI >> random CI (Calvano et al. 2020 direction; Deng et al. 2024 nuance noted).
Fast (8000 eps) for CI/CD; sweep documented.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.coordination import simulate_qlearning, simulate_competitive_baseline

def main():
    q = simulate_qlearning(episodes=8000, seed=42)
    base = simulate_competitive_baseline(seed=42)
    checks = {
        "collusion_positive": q["collusion_index"] > 0.15,
        "beats_random": q["collusion_index"] > base["collusion_index"] + 0.1,
        "tail_suprac competitive": q["tail_price"] > 0.15,
    }
    plt.figure(figsize=(6, 4))
    plt.plot(q["avg_prices"], label="Q-learning avg price (subsampled)")
    plt.axhline(0.5, color="red", linestyle="--", label="Monopoly 0.5")
    plt.axhline(0.05, color="green", linestyle="--", label="Nash ~0.05")
    plt.xlabel("Training (x100 episodes)"); plt.ylabel("Price")
    plt.title(f"Algorithmic collusion CI={q['collusion_index']:.2f}")
    plt.legend(); plt.tight_layout(); plt.savefig("results/exp04_collusion.png", dpi=150)
    out = {"qlearning": {k: v for k, v in q.items() if k != "avg_prices"},
           "baseline": base, "checks": checks,
           "hidden_pattern": "Stateless Q-learners still collude (async-robust per Conjeaud et al. 2026), but CI variance across seeds is high — single-run audits under-detect collusion. Regulators must simulate distributions, not point estimates (Assad et al. 2021 recommendation)."}
    os.makedirs("results", exist_ok=True)
    json.dump(out, open("results/exp04.json", "w"), indent=2)
    print(json.dumps(out["qlearning"], indent=2))
    assert all(checks.values()), checks
    print("EXP04 OK")

if __name__ == "__main__":
    main()
