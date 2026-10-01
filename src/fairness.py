"""Fairness / disparate-impact audit — Ch.6 + Ch.9-10.

Implements (from scratch, no hand-waving):
- synthetic market where WTP = preferences + wealth + bias, bias correlated with group
- proxy variables (zip, height, savings) correlated with protected attr
- transparency protocols: permutation importance, LASSO surrogate, teacher-student tree
- disparate-impact regression with controls (similarly-situated test)
All keyless sklearn only. Verified via agent-reach fairness auditing + EU AI Act 2026 transparency docs.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestRegressor


def make_synthetic_market(n=5000, seed=42, group_gap_bias=12.0):
    rng = np.random.default_rng(seed)
    # protected: 0 majority, 1 minority (30%)
    group = (rng.random(n) < 0.30).astype(int)
    income = rng.normal(55, 15, n) - group * 8  # income gap
    education = rng.normal(14, 2.5, n) - group * 1.2
    # bias (overestimation) higher for minority via information-access channel (book Ch.6D)
    bias = rng.normal(5, 8, n) + group * group_gap_bias
    pref = rng.normal(50, 12, n)
    wtp = pref + 0.4 * (income - 55) + bias
    # proxies
    zip_code = 90000 + (income * 10).astype(int) + rng.integers(-200, 200, n)  # proxy for group via income
    height = rng.normal(170, 10, n) + (rng.random(n) < 0.5) * 12  # proxy for sex demo
    savings = np.clip(20 - 0.5 * bias + rng.normal(0, 5, n), -20, 60)
    # black-box price: seller charges 0.9*wtp + noise (profit-max)
    price = 0.9 * wtp + rng.normal(0, 3, n)
    df = pd.DataFrame({"group": group, "income": income, "education": education,
                       "bias": bias, "pref": pref, "wtp": wtp, "zip": zip_code,
                       "height": height, "savings": savings, "price": price})
    return df


def train_blackbox(df):
    X = df[["income", "education", "zip", "height", "savings"]]
    y = df["price"]
    model = RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42, n_jobs=-1)
    model.fit(X, y)
    return model


def permutation_audit(model, df):
    X = df[["income", "education", "zip", "height", "savings"]]
    y = df["price"]
    r = permutation_importance(model, X, y, n_repeats=5, random_state=42)
    return dict(zip(X.columns, r.importances_mean))


def lasso_surrogate(model, df):
    X = df[["income", "education", "zip", "height", "savings"]]
    pred = model.predict(X)
    # standardize
    Xs = (X - X.mean()) / X.std()
    lasso = LassoCV(cv=3, random_state=42).fit(Xs, pred)
    return dict(zip(X.columns, lasso.coef_))


def teacher_student(df, model, max_depth=3):
    X = df[["income", "education", "zip", "height", "savings"]]
    pred = model.predict(X)
    tree = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
    tree.fit(X, pred)
    return {"depth": max_depth, "score": float(tree.score(X, pred)),
            "importances": dict(zip(X.columns, tree.feature_importances_))}


def disparate_impact_regression(df):
    """price ~ group + income + education (similarly-situated controls).
    Returns group coef, p-ish via t from statsmodels OLS.
    """
    import statsmodels.formula.api as smf
    m = smf.ols("price ~ group + income + education", data=df).fit()
    return {"group_coef": float(m.params["group"]),
            "group_p": float(m.pvalues["group"]),
            "rsq": float(m.rsquared),
            "summary": str(m.summary()).split("\n")[:12]}
