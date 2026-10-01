"""BBP two-period model — exact replication of Book Ch.2 Appendix (uniform [0,V]).

U markets: consumers unaware, threshold = p1.
S markets: strategic, threshold tv1 = 2*p1, pH2=2*p1, pL2=p1.
Verified: Porat (2026) JLS BBP + websearch Harvard Olin DP formulas.
"""
from dataclasses import dataclass


@dataclass
class BBPResult:
    p1: float
    pH2: float
    pL2: float
    profit: float
    cs: float
    groups: dict


def bbp_U(V=100.0):
    # Book: p1=4V/7, pH2=4V/7, pL2=2V/7
    p1 = 4 * V / 7
    pH2 = 4 * V / 7
    pL2 = 2 * V / 7
    # profits: pi1+piH2+piL2 = 28/49 V
    profit = 28 / 49 * V
    cs = 11 / 49 * V
    # No-BBP baseline: profit 0.5V, cs 0.25V
    groups = {
        "v in [4V/7,V]": {"cs_no": 96 / 392 * V, "cs_bbp": 72 / 392 * V},
        "v in [V/2,4V/7]": {"cs_no": 2 / 392 * V, "cs_bbp": 7 / 392 * V},
        "v in [2V/7,V/2]": {"cs_no": 0.0, "cs_bbp": 9 / 392 * V},
        "v in [0,2V/7]": {"cs_no": 0.0, "cs_bbp": 0.0},
    }
    return BBPResult(p1, pH2, pL2, profit, cs, groups)


def bbp_S(V=100.0):
    # Book: p1=3V/10, tv1=6V/10, pH2=6V/10, pL2=3V/10
    p1 = 3 * V / 10
    pH2 = 6 * V / 10
    pL2 = 3 * V / 10
    profit = 0.45 * V
    cs = 0.325 * V
    groups = {
        "v in [6V/10,V]": {"cs_no": 0.24 * V, "cs_bbp": 0.28 * V},
        "v in [V/2,6V/10]": {"cs_no": 0.01 * V, "cs_bbp": 0.025 * V},
        "v in [3V/10,V/2]": {"cs_no": 0.0, "cs_bbp": 0.02 * V},
        "v in [0,3V/10]": {"cs_no": 0.0, "cs_bbp": 0.0},
    }
    return BBPResult(p1, pH2, pL2, profit, cs, groups)


def bbp_baseline(V=100.0):
    return {"profit": 0.5 * V, "cs": 0.25 * V, "p": V / 2}
