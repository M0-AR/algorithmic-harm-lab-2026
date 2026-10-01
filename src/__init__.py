from .demand import MarketParams, monopoly_no_discrimination, perfect_price_discrimination, imperfect_segmentation_surplus
from .bbp import bbp_U, bbp_S, bbp_baseline
from .targeting import TargetParams, targeting_over, targeting_under
from .coordination import simulate_qlearning, simulate_competitive_baseline
from .fairness import make_synthetic_market, train_blackbox, permutation_audit, lasso_surrogate, teacher_student, disparate_impact_regression
from .live_data import fetch_avb_monthly, fetch_fx, fetch_ftc_realpage_head
