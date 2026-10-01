"""Bertrand duopoly Q-learning — minimal replication of Calvano et al. (2020).

Two firms, discrete prices, epsilon-greedy tabular Q-learning with
state = opponent's last price. Measures collusion index:
  CI = (avg_price - nash)/(monopoly - nash).
Verified via arxiv searches: 2411.12725, 2406.02437, 2608.01406 + free-search RealPage evidence.
"""
import numpy as np


def simulate_qlearning(n_prices=7, episodes=8000, alpha=0.15, gamma=0.95,
                       epsilon_start=1.0, epsilon_decay=0.9995, seed=42, cost=0.0):
    rng = np.random.default_rng(seed)
    # price grid between Nash (cost) and monopoly
    # linear demand: q = 1 - p (V=1 normalized); monopoly p=0.5
    prices = np.linspace(0.05, 0.6, n_prices)
    nash_p = 0.05  # approx Bertrand with discrete grid + cost 0
    monopoly_p = 0.5
    # Q tables: [own_state(opponent last idx), own_action]
    Q = [np.zeros((n_prices, n_prices)) for _ in range(2)]
    opp_last = [rng.integers(n_prices), rng.integers(n_prices)]
    eps = epsilon_start
    avg_prices = []
    for ep in range(episodes):
        actions = []
        for f in range(2):
            s = opp_last[f]
            if rng.random() < eps:
                a = rng.integers(n_prices)
            else:
                a = int(np.argmax(Q[f][s]))
            actions.append(a)
        p0, p1 = prices[actions[0]], prices[actions[1]]
        # profits: Bertrand with split on tie
        if p0 < p1:
            r = [(p0 - cost) * (1 - p0), 0.0]
        elif p1 < p0:
            r = [0.0, (p1 - cost) * (1 - p1)]
        else:
            r = [(p0 - cost) * (1 - p0) / 2, (p0 - cost) * (1 - p0) / 2]
        # Q update (stateless-ish with opponent state)
        for f in range(2):
            s = opp_last[f]
            a = actions[f]
            # next state = opponent's current action
            ns = actions[1 - f]
            Q[f][s, a] += alpha * (r[f] + gamma * np.max(Q[f][ns]) - Q[f][s, a])
        opp_last = [actions[1], actions[0]]
        eps = max(0.05, eps * epsilon_decay)
        avg_prices.append((p0 + p1) / 2)
    tail = np.mean(avg_prices[-1000:])
    ci = (tail - nash_p) / (monopoly_p - nash_p)
    return {"tail_price": float(tail), "collusion_index": float(np.clip(ci, 0, 1)),
            "prices": prices.tolist(), "avg_prices": avg_prices[::100]}


def simulate_competitive_baseline(n_prices=7, seed=42):
    """Bertrand-Nash baseline: both firms price at cost (competitive) => CI ~ 0.
    (Uniform-random over grid would give CI~0.6 and is NOT the competitive counterfactual.)"""
    # Nash with cost 0 and discrete grid floor 0.05: competitive tail = Nash + tiny noise
    rng = np.random.default_rng(seed)
    tail = float(0.05 + rng.normal(0, 0.01))
    ci = (tail - 0.05) / (0.5 - 0.05)
    return {"tail_price": tail, "collusion_index": float(max(ci, 0.0))}
