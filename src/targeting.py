"""Targeting model Ch.3 + Appendix — over/underestimation with threshold alpha_hat.

Over: CSA = aU(1-g)b1 + aB(1-d*g)b2 ; pre: P1 to all if aB<ahat else P2 to biased only.
Under: CSA = aU(1-g)b1 + aB(1-g)b2 ; always helps vs pre.
ahat_over = (g*b1-c)/(g*d*b2-c); ahat_under_B = 1-(g*b2-c)/(g*b1-c)
"""
from dataclasses import dataclass


@dataclass
class TargetParams:
    b1: float = 200.0
    b2: float = 100.0
    delta: float = 3.0  # over: perceived b2*delta ; under: perceived b1*delta (delta<1)
    gamma: float = 0.5
    c: float = 0.0
    alphaB: float = 0.5


def targeting_over(tp: TargetParams):
    b1, b2, d, g, c, aB = tp.b1, tp.b2, tp.delta, tp.gamma, tp.c, tp.alphaB
    aU = 1 - aB
    piA = aU * (g * b1 - c) + aB * (g * d * b2 - c)
    csA = aU * (1 - g) * b1 + aB * (1 - d * g) * b2
    ahat = (g * b1 - c) / (g * d * b2 - c) if (g * d * b2 - c) != 0 else 1.0
    # pre-algorithmic
    if aB < ahat:
        cs_pre = (1 - g) * b1
        pre_desc = "P1 to all"
        pi_pre = g * b1 - c
    else:
        cs_pre = aB * (1 - d * g) * b2
        pre_desc = "P2 to biased only"
        pi_pre = aB * (g * d * b2 - c)
    helps = csA > cs_pre
    return {"piA": piA, "csA": csA, "cs_pre": cs_pre, "ahat": ahat,
            "pre_desc": pre_desc, "helps": helps}


def targeting_under(b1=300.0, b2=200.0, delta=1/3, gamma=0.5, c=0.0, alphaB=0.5):
    """Example 3.2: b1=300 hybrid, b2=200 guzzler, perceived b1=100."""
    aU = 1 - alphaB
    piA = aU * (gamma * b1 - c) + alphaB * (gamma * b2 - c)
    csA = aU * (1 - gamma) * b1 + alphaB * (1 - gamma) * b2
    ahatU = (gamma * b2 - c) / (gamma * b1 - c)
    ahatB = 1 - ahatU
    if alphaB > ahatB:  # equivalently aU < ahatU
        cs_pre = (1 - gamma) * b2
        pre_desc = "P2 to all"
    else:
        cs_pre = aU * (1 - gamma) * b1
        pre_desc = "P1 to unbiased only"
    return {"piA": piA, "csA": csA, "cs_pre": cs_pre, "ahatB": ahatB,
            "pre_desc": pre_desc, "helps": csA > cs_pre}
