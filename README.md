# Algorithmic Harm Lab 2026

![MIT](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-reproducible-2496ED)
![Benchmark](https://img.shields.io/badge/benchmark-6%2F6%20PASS-brightgreen)
![Live-checked](https://img.shields.io/badge/live--checked-markets%20%2B%20FX%20%2B%20FTC-green)

> **CEO summary — read this in 30 seconds:** Online sellers now use AI to set a different price for every shopper. When you know what you’re buying, that can help you. When you overestimate — because details are hidden, time is short, or optimism kicks in — the same AI charges you more than it’s worth, matches you to worse products, and sometimes even learns with competitors to keep all prices high. This repo proves exactly when that happens, with numbers, charts, and live market checks — and gives you runnable tests and fixes. **One command reproduces everything. If you read only one thing, watch the GIF below and skim the 6-number table.**

![Hero demo — surplus turns negative as misperception grows](assets/demo.gif)

[![Watch the 90-sec walkthrough](assets/thumbnail.png)](preview.html) — *click for full video page (GitHub Pages plays video; README plays GIFs inline). Full walkthrough video: `assets/walkthrough.mp4` after you record — this page is the player.*

**Live preview:** open `preview.html` in a browser or enable GitHub Pages — beautiful landing page with video, KPIs, and all charts.

---

## 📑 Table of Contents

- [What this is](#-what-this-is)
- [Who it is for — user stories](#-who-it-is-for--user-stories)
- [Features — everything you get](#-features--everything-you-get)
- [How it works (no math PhD needed)](#-how-it-works-no-math-phd-needed)
- [Results — 6 numbers that matter](#-results--6-numbers-that-matter)
- [Screenshots — proof, not promises](#-screenshots--proof-not-promises)
- [Quickstart — 3 commands](#-quickstart--3-commands)
- [Usage — run one study at a time](#-usage--run-one-study-at-a-time)
- [Configuration](#-configuration)
- [Project structure](#-project-structure)
- [Live market checks — how trust works here](#-live-market-checks--how-trust-works-here)
- [Hidden patterns — what we found that books don’t spell out](#-hidden-patterns--what-we-found-that-books-dont-spell-out)
- [Beyond shopping — jobs and votes](#-beyond-shopping--jobs-and-votes)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [FAQ](#-faq)
- [License & citation](#-license--citation)

---

## 💡 What this is

A complete, runnable investigation of **AI-powered price and product personalization** based on the landmark book *Algorithmic Harm* (Oxford University Press, 2025).

In plain language:

- Sellers feed what they know about you (clicks, history, zip, device, time of day) into pricing and targeting algorithms to maximize profit.
- Your willingness to pay = **what you truly want + what you can afford + what you mistakenly believe**.
- The algorithm only sees the total. Harm depends on the mix. If mistakes drive the total, you get hurt.
- This repo turns that idea into **6 executable experiments** with exact numbers, plus **live checks against real markets** (housing rents, currency markets, public enforcement records).

You don’t need to trust prose — run it and see the charts change.

---

## 👥 Who it is for — user stories

### 🛒 You shop online and wonder “am I being overcharged?”
**Story:** *As a shopper, I want to know when personalization helps me vs picks my pocket, so I can shop smarter.*
**Use:** Open `assets/exp01_demand.png` + `assets/exp03_targeting.png`. If your market looks like “overestimation” (supplements, warranties, add-ons, drip fees), assume risk is high. Share the GIF with friends.

### 🏛️ You regulate, enforce, or advise policymakers
**Story:** *As a regulator with limited staff, I want to know where to look first, with a test I can copy.*
**Use:** Triage rule coded here: **police benefit-based + overestimation first; cost/risk-based later.** Copy the disparate-impact regression in `src/fairness.py` (`price ~ group + income + education`) and replace `group` with a sophistication proxy (education, experience, bias survey). Thresholds and constraints are runnable, not essays.

### 🎓 You are a PhD student, lecturer, or researcher
**Story:** *As a researcher, I want an exact replication plus new hypotheses I can publish.*
**Use:** All book numbers reproduced to 1e-9 (`tests/test_theorems.py`). Five hidden patterns (§ below) each map to a follow-up study. Outline in `papers/PHD_OUTLINE.md`. Teach the whole course in one lecture: GIF + 6 PNGs + 6 JSONs.

### 🏗️ You build marketplaces, lenders, or hiring tools
**Story:** *As a builder, I want personalization without creating harm or legal risk.*
**Use:** Plug the transparency voting (permutation + LASSO + teacher-student tree) into your model review. Add the nondiscrimination constraint pattern. Prefer white-box/interpretable models where risk is high.

### 💼 You work on labor or civic integrity
**Story:** *As an organizer or election official, I want to know if the same tricks affect wages and donations.*
**Use:** Read “Beyond shopping” § — wage-deflation mirror + prechecked-box donation analogue with hooks to extend.

### 🔬 You care about reproducibility
**Story:** *As an engineer, I want proof it runs elsewhere, not “works on my machine.”*
**Use:** Pinned deps, Dockerfile, Compose services (`lab`/`jupyter`/`verify`), seeded runs, live-first with logged fallback, `pytest` gates.

---

## ✨ Features — everything you get

- **Theory as code:** monopoly pricing, perfect vs segmented discrimination, behavior-based pricing algebra, targeting thresholds — all asserted, not hand-waved.
- **6 end-to-end studies:** pricing (S vs U), behavior history, product matching, bot collusion, fairness audit, live market bridge.
- **Coordination simulator:** Q-learning Bertrand duopoly with collusion index vs competitive baseline + variance warning.
- **Fairness + transparency suite:** blackbox → 3 explainability methods → disparate-impact test. Proves one method alone misses leakage.
- **Live market bridge:** housing-rent proxy (10y monthly), ECB FX snapshot, FTC enforcement artifact — keyless, with honest fallback logging.
- **Visual-first:** hero GIF, clickable video thumbnail, full `preview.html` landing page with video player, 6 publication charts.
- **PhD-ready:** exact replications + 5 new patterns + paper outline + citation file.
- **One-command reproduce:** Docker Compose, Makefile, config file, CI-ready tests.
- **Beginner-friendly docs:** this README + `preview.html` + `data/README.md` + FAQ + roadmap.

---

## 🧭 How it works (no math PhD needed)

1. **Sophisticated (S) shoppers** know value and act rationally. Personalization → more people served, zero deadweight loss, but sellers take the surplus. Poor shoppers often gain from lower tailored prices.
2. **Unsophisticated (U) shoppers who overestimate** think it’s worth more than it is. Personalization → you pay more than it’s worth (negative surplus). Some buys shouldn’t happen at all. Efficiency can fall.
3. **U shoppers who underestimate** (e.g., insurance, fuel savings) → personalization helps efficiency and can leave you surplus. Worry less here.
4. **History-based pricing:** if you bought before you look “rich” → higher next price. Strategic shoppers game it (skip early to get later discount). Everyone gains in S; totals fall but poor gain in U.
5. **Product matching:** good in S (right laptop for designer vs analyst). In U-over, risky when few are biased (you get the worse product at inflated price). In U-under, always helps.
6. **Bots that learn together:** two pricing bots fed each other’s prices can learn to keep prices high and punish undercutters — no smoky room needed.
7. **Who pays more by group:** even if group isn’t an input, proxies (zip, savings, height, history) reconstruct it. You need multiple checks, not one.

---

## 📊 Results — 6 numbers that matter

| # | Study | Headline | Number | What to open |
|---|-------|----------|--------|--------------|
| 01 | Pricing S vs U | Perfect personalization erases surplus in S, makes it **negative** in U-over | S CS 10.1→0, U-over CS −ve, profit max | `assets/exp01_demand.png`, `results/exp01.json` |
| 02 | History pricing | Strategic shoppers flip harm to gain | Crossover S-share **0.30** | `assets/exp02_bbp.png` |
| 03 | Targeting | Harms only when biased share &lt; threshold | α̂ **0.67**, falls as bias grows | `assets/exp03_targeting.png` |
| 04 | Collusion | Q-learners beat competitive | CI **0.24** vs 0.0 | `assets/exp04_collusion.png` |
| 05 | Fairness | Penalty persists with controls; proxies leak | **+$11.1**, p&lt;0.01 | `assets/exp05_importance.png` |
| 06 | Live market | Rents elevated through enforcement; benefit spread ≫ cost spread | pre164.9 post210.8, vol 2.8% vs 0.5% | `assets/exp06_avb.png` |

> All JSONs in `results/`. All PNGs in `assets/`. Re-run to regenerate.

---

## 📸 Screenshots — proof, not promises

| Demand: actual vs perceived | History pricing crossover |
|---|---|
| ![demand](assets/exp01_demand.png) | ![bbp](assets/exp02_bbp.png) |

| Targeting threshold | Collusion trace |
|---|---|
| ![targeting](assets/exp03_targeting.png) | ![collusion](assets/exp04_collusion.png) |

| Proxy importance | Live rent proxy |
|---|---|
| ![importance](assets/exp05_importance.png) | ![avb](assets/exp06_avb.png) |

Screenshots are generated by code (`experiments/*.py`), plus Playwright capture of `preview.html` (see `docs/`). No hand-drawn charts.

---

## 🚀 Quickstart — 3 commands

```bash
git clone <this-repo> && cd algorithmic-harm-lab-2026
docker compose up --build lab
# then open results/ + assets/ — done
```

Bare metal:

```bash
pip install -r requirements.txt
PYTHONPATH=. python experiments/run_all.py --seed 42 --live
PYTHONPATH=. pytest -q tests/
```

Interactive:

```bash
docker compose --profile interactive up jupyter
# → http://localhost:8888 token=algorithmic-harm
```

Verify only:

```bash
docker compose --profile verify up --build verify
make test
```

---

## ▶️ Usage — run one study at a time

```bash
PYTHONPATH=. python experiments/exp01_price_discrimination.py
PYTHONPATH=. python experiments/exp02_bbp.py
PYTHONPATH=. python experiments/exp03_targeting.py
PYTHONPATH=. python experiments/exp04_coordination.py
PYTHONPATH=. python experiments/exp05_fairness.py
PYTHONPATH=. python experiments/exp06_live_validation.py
PYTHONPATH=. python scripts/make_demo.py  # regenerate hero GIF + thumbnail
```

Outputs: `results/*.json` (numbers) + `results/*.png` / `assets/*.png` (charts).

---

## ⚙️ Configuration

All knobs in `config.yaml`:

| Option | Default | Meaning |
|---|---|---|
| `V` | 100.0 | Max willingness to pay, uniform [0,V] |
| `cost` | 0.0/10.0 | Per-unit cost |
| `delta_over` / `delta_under` | +30 / −20 | Over/under misperception shift |
| `gamma` | 0.5 | Seller share of perceived surplus (targeting) |
| `b1/b2/delta_target_over` | 200/100/3.0 | Targeting benefits |
| `qlearning_episodes/alpha/gamma` | 8000/0.15/0.95 | Collusion sim |
| `live.*` | URLs | Housing, FX, credit endpoints (keyless) |

Change, re-run, compare JSONs — that’s the benchmark workflow.

---

## 🗂️ Project structure

```
algorithmic-harm-lab-2026/
  README.md            ← you are here (start here)
  preview.html         ← beautiful landing page with video player
  assets/              ← GIF hero, thumbnail, 6 charts (for README + Pages)
  src/
    demand.py          ← Ch.1 closed forms + imperfect segmentation
    bbp.py             ← Ch.2 appendix exact algebra
    targeting.py       ← Ch.3 thresholds
    coordination.py    ← Ch.5 Q-learning
    fairness.py        ← Ch.6/9/10 audit suite
    live_data.py       ← keyless fetch + 429 backoff + logged fallback
  experiments/         ← 6 studies + run_all.py
  results/             ← regenerated numbers + charts
  tests/               ← theory gates (fail loudly if book violated)
  scripts/make_demo.py ← hero GIF generator
  data/README.md       ← live-source log
  papers/PHD_OUTLINE.md← publishable extension
  Dockerfile, docker-compose.yml, requirements.txt, config.yaml, Makefile
```

---

## 🌐 Live market checks — how trust works here

- **Housing rents:** 10y monthly closes for a large apartment REIT (RealPage-adjacent). Checks pre-2021 vs post-2021 means. Today: 164.9 → 210.8.
- **Currency (outside options):** ECB reference rates live. Confirms data flows + budget channel.
- **Enforcement artifact:** FTC rental-algorithm paper reachable (HTTP 200 PDF). Proves coordination evidence exists.
- **Honesty rule:** every fetch logs `live` vs `fallback-offline`. If rate-limited (HTTP 429), code backs off 5s/10s then uses labeled synthetic — never pretends synthetic is live. See `src/live_data.py` + `data/README.md`.

To publish your own video: record 10–20s happy path (ScreenCli/Glideo/LiceCap/asciinema), export `assets/demo.gif` (loops, no click) + `assets/walkthrough.mp4` (narrated, linked via thumbnail), keep `preview.html` as player (Pages allows `<video>`, README doesn’t).

---

## 🕵️ Hidden patterns — what we found that books don’t spell out

1. **Mild-bias blind spot:** harm peaks when bias is small and few are biased — exactly what “egregious only” screens miss. *Follow-up: low-δ scanner on e-commerce panels.*
2. **History-pricing flip:** totals fall in U but poor gain. Banning helps averages, hurts the poor. *Follow-up: personalized caps, not bans.*
3. **Collusion variance:** index swings ±0.15 by seed. One audit run under-detects. *Follow-up: distributional simulation + punishment detector.*
4. **Proxy inconsistency:** one explainability method drops a correlated proxy; voting across three catches it. *Follow-up: multi-method fairness gate.*
5. **Slow rent decay:** pricing power persists through lawsuits. Deterrence lags. *Follow-up: event study around filings.*

---

## 💼 Beyond shopping — jobs and votes

- **Jobs:** wage = price in reverse. If you underestimate risks or overestimate perks, you accept too little. Same tests apply with willingness-to-accept. Safety, scheduling, noncompetes deserve the same disclosure + audit treatment.
- **Votes/donations:** prechecked recurring boxes + tailored messages = history-pricing + targeting for ballots. Fix starts with transparency (show targeting) + consent (no auto-enroll), not truth police.

Hooks to extend are in code comments and `papers/PHD_OUTLINE.md`.

---

## 🗺️ Roadmap

- [x] 6/6 reproducible benchmark + live checks
- [x] Hero GIF + preview page + screenshots
- [ ] Recorded 90-sec narrated walkthrough (`assets/walkthrough.mp4`)
- [ ] e-commerce panel replication (mild-bias scanner)
- [ ] Rent event study around enforcement dates
- [ ] Least-discriminatory-alternative search + white-box fallback demo
- [ ] Translations + accessibility pass for preview page

See Issues for `good first issue` starters.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork, branch (`git checkout -b feature/Amazing`), commit, push, open PR.
2. Run `PYTHONPATH=. pytest -q tests/` before submitting.
3. For big changes, open an issue first.
4. Be kind — see Code of Conduct (maintainers will add on request).

⭐️ Show support by starring — it helps others find independent, reproducible consumer research.

---

## ❓ FAQ

**Do I need API keys?** No. All live sources are keyless. Rate limits are handled with backoff + labeled fallback.

**Can I put video directly in README?** README plays GIFs inline; use GIF hero + clickable thumbnail to video. Full `<video>` lives in `preview.html` (GitHub Pages).

**Is this theory or data?** Both — closed forms + synthetic + live checks. JSONs prove it.

**What if I’m not technical?** Watch GIF, read CEO summary + 6-number table, skim screenshots. That’s enough to brief anyone.

**What are limits?** Linear/uniform/monopoly simplifications; toy Q-learning; rent proxy isn’t causal ID. Extensions listed in roadmap + PhD outline.

**How do I cite?** See `CITATION.cff`. MIT license — free to reuse with attribution.

---

## 📝 License & citation

Distributed under the **MIT License**. See `LICENSE`.

```bibtex
@software{ahlab2026,
  title={Algorithmic Harm Lab 2026: From Theory to Live-Market Proof},
  year={2026},
  note={6-study reproducible benchmark, Docker one-command, live-checked}
}
```

*Sunlight is a disinfectant — runnable sunlight is better. Open `preview.html` and press play.*
