"""Theorem tests — mirror book propositions (fail loudly if theory violated)."""
from src.demand import MarketParams, monopoly_no_discrimination, perfect_price_discrimination
from src.bbp import bbp_U, bbp_S, bbp_baseline
from src.targeting import TargetParams, targeting_over, targeting_under

def test_S_theorem():
    s_no = monopoly_no_discrimination(MarketParams(100, 10, 0.0))
    s_pd = perfect_price_discrimination(MarketParams(100, 10, 0.0))
    assert abs(s_pd["cs"]) < 1e-9 and abs(s_pd["dwl"]) < 1e-9
    assert s_pd["profit"] > s_no["profit"]

def test_U_over_worse():
    s_pd = perfect_price_discrimination(MarketParams(100, 10, 0.0))
    u_pd = perfect_price_discrimination(MarketParams(100, 10, 30.0))
    assert u_pd["cs"] < 0 and u_pd["cs"] < s_pd["cs"]

def test_bbp_numbers():
    u, s, b = bbp_U(100), bbp_S(100), bbp_baseline(100)
    assert abs(u.profit - 28/49*100) < 1e-9 and abs(u.cs - 11/49*100) < 1e-9
    assert abs(s.profit - 0.45*100) < 1e-9 and abs(s.cs - 0.325*100) < 1e-9
    assert u.profit > b["profit"] > s.profit and s.cs > b["cs"] > u.cs

def test_targeting_book_examples():
    a = targeting_over(TargetParams(alphaB=0.5))
    assert abs(a["piA"] - 125) < 1e-9 and abs(a["csA"] - 25) < 1e-9 and not a["helps"]
    b = targeting_over(TargetParams(alphaB=0.75))
    assert b["helps"]
    c = targeting_under(alphaB=0.5)
    assert c["helps"]
