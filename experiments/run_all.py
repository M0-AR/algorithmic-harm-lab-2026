"""Run all experiments in order — single entrypoint for Docker (AEA pattern)."""
import argparse, sys, traceback
from experiments.exp01_price_discrimination import main as e01
from experiments.exp02_bbp import main as e02
from experiments.exp03_targeting import main as e03
from experiments.exp04_coordination import main as e04
from experiments.exp05_fairness import main as e05
from experiments.exp06_live_validation import main as e06

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--skip-live", action="store_true")
    a = ap.parse_args()
    import numpy as np, random
    np.random.seed(a.seed); random.seed(a.seed)
    fns = [("EXP01", e01), ("EXP02", e02), ("EXP03", e03), ("EXP04", e04), ("EXP05", e05)]
    if not a.skip_live:
        fns.append(("EXP06-live", e06))
    ok = {}
    for name, fn in fns:
        try:
            print(f"\n===== {name} =====")
            fn(); ok[name] = "PASS"
        except Exception as e:
            print(f"{name} FAILED: {e}"); traceback.print_exc(); ok[name] = f"FAIL: {e}"
    print("\n===== SUMMARY =====")
    for k, v in ok.items():
        print(f"{k}: {v}")
    if any(v != "PASS" for v in ok.values()):
        sys.exit(1)
    print("\nAll benchmarks PASS — reproducible (World Bank RRR + AEA Docker pattern).")

if __name__ == "__main__":
    main()
