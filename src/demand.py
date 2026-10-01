"""Core demand/pricing theorems — faithful to Bar-Gill & Sunstein Ch.1-2.

Verified against:
- websearch: Bar-Gill Sunstein Harvard Olin DP 1091 (2023) + SSRN 5162465
- free-search: RealPage/FTC 2026 rental algo evidence
- arxiv: Q-learning collusion (Askenazi-Golan et al. 2411.12725, Deng et al. 2406.02437)
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class MarketParams:
    V: float = 100.0
    cost: float = 0.0
    delta: float = 0.0  # misperception shift: perceived w = v + delta


def monopoly_no_discrimination(p: MarketParams):
    """Uniform monopoly price under (possibly misperceived) demand.

    Demand: q(price) = (V + delta - price)/V for price in [delta, V+delta].
    Monopoly: max_p p*q - c*q  => p* = (V+delta+c)/2
    Returns dict with price, quantity, consumer surplus (ACTUAL), profit, dwl.
    """
    V, c, d = p.V, p.cost, p.delta
    pm = (V + d + c) / 2.0
    qm = (V + d - pm) / V  # = (V+d-c)/(2V)
    qm = float(np.clip(qm, 0, 1))
    # Actual CS: integrate (v - pm) over buyers (v >= pm - d)
    cutoff = pm - d
    if cutoff >= V:
        cs = 0.0
    else:
        lo = max(cutoff, 0.0)
        # E[(v-pm)+ | v>=lo] with uniform: integral_lo^V (v-pm)/V dv
        cs = ((V - lo) * ((V + lo) / 2 - pm)) / V
    profit = (pm - c) * qm
    # First-best quantity: all v>=c buy => qfb = (V-c)/V
    qfb = max((V - c) / V, 0.0)
    # DWL components: under-consumption triangle + over-consumption triangle
    # Compute total surplus at qm vs first-best via integration
    # Total surplus per buyer v: (v - c); buyers are v in [lo, V]
    ts_qm = ((V - lo) * ((V + lo) / 2 - c)) / V if V > lo else 0.0
    ts_fb = ((V - max(c, 0)) * ((V + max(c, 0)) / 2 - c)) / V if V > c else 0.0
    dwl = ts_fb - ts_qm
    # competitive benchmark
    pc = c
    qc = qfb
    return {"pm": pm, "qm": qm, "cs": cs, "profit": profit, "dwl": dwl,
            "pc": pc, "qc": qc, "cutoff": cutoff}


def perfect_price_discrimination(p: MarketParams):
    """Each consumer charged perceived w = v+delta (just below).
    Profit = E[w - c | w>=c]; Actual CS = E[v - w | w>=c] = -delta * P(buy).
    Efficiency: buys iff v+delta >= c => cutoff v >= c-delta.
    """
    V, c, d = p.V, p.cost, p.delta
    cutoff = c - d
    lo = np.clip(cutoff, 0, V)
    prob_buy = (V - lo) / V
    # profit: E[v+d-c | v>=lo]
    avg_v = (V + lo) / 2 if V > lo else 0.0
    profit = prob_buy * (avg_v + d - c)
    cs = prob_buy * (avg_v - (avg_v + d))  # = -d * prob_buy
    # total surplus
    ts = prob_buy * (avg_v - c)
    # first best
    fb_lo = np.clip(c, 0, V)
    fb_prob = (V - fb_lo) / V
    fb_avg = (V + fb_lo) / 2 if V > fb_lo else 0.0
    ts_fb = fb_prob * (fb_avg - c)
    dwl = ts_fb - ts
    return {"profit": float(profit), "cs": float(cs), "prob_buy": float(prob_buy),
            "total": float(ts), "dwl": float(dwl), "cutoff": float(cutoff)}


def imperfect_segmentation_surplus(V=100.0, c=0.0, delta=0.0, n_segments=4):
    """Group-based (imperfect) PD: split perceived-WTP distribution into n equal groups.
    Within each group charge min perceived WTP of group. Returns (cs, profit).
    Demonstrates book claim: imperfect PD leaves positive CS in S, negative tail in U.
    """
    # perceived w ~ Uniform[delta, V+delta]
    bounds = np.linspace(delta, V + delta, n_segments + 1)
    cs_tot, prof_tot = 0.0, 0.0
    for i in range(n_segments):
        price = bounds[i]  # lowest w in segment (serve whole segment)
        # buyers: all in segment with w>=c and w>=price (by construction) and v arbitrary
        # segment corresponds to v in [bounds[i]-delta, bounds[i+1]-delta] intersect [0,V]
        v_lo = max(bounds[i] - delta, 0)
        v_hi = min(bounds[i + 1] - delta, V)
        if v_hi <= v_lo:
            continue
        mass = (v_hi - v_lo) / V
        avg_v = (v_lo + v_hi) / 2
        if price < c:
            # seller would skip segment
            continue
        cs_tot += mass * (avg_v - price)
        prof_tot += mass * (price - c)
    return {"cs": cs_tot, "profit": prof_tot}
