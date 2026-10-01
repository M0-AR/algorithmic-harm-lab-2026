# Data — live-first, fallback-documented (World Bank RRR compliant)

All experiments attempt LIVE fetch first (keyless), then fall back to
synthetic offline bundle with `source` logged in `results/exp06.json`.

| Stream | Live URL | Why |
|---|---|---|
| AVB rents proxy | `https://query1.finance.yahoo.com/v8/finance/chart/AVB?interval=1mo&range=5y` | AvalonBay SEC CIK 915912 (found via openresearch sec_filings); RealPage-era pricing power |
| FX outside-options | `https://api.frankfurter.app/latest?from=USD&to=EUR,GBP,JPY` | ECB reference; budget-constraint channel |
| FTC rental-algo paper | `https://www.ftc.gov/system/files/ftc_gov/pdf/calder-wang_rental_algo_2026_2_24_ftc.pdf` | Assad/Clark/Ershov/Xu lineage; German gasoline + US rentals evidence (free-search) |
| German Credit | UCI archive URL in config | cost-based vs benefit-based split demo |

No keys required. No522 local-repo data reused — everything from scratch.
