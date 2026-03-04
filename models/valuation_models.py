import numpy as np


# --------------------------------------------------
# Revenue Multiple Model
# --------------------------------------------------

def revenue_multiple_model(
    revenue,
    shares_outstanding,
    ev_revenue_multiple,
    net_debt=0
):
    """
    Growth valuation using EV / Revenue multiple.
    Works for unprofitable companies.

    revenue: latest annual revenue
    shares_outstanding: total shares
    ev_revenue_multiple: sector EV/Revenue multiple
    net_debt: debt - cash
    """

    enterprise_value = revenue * ev_revenue_multiple

    equity_value = enterprise_value - net_debt

    price_per_share = equity_value / shares_outstanding

    return price_per_share


# --------------------------------------------------
# Rule of 40 Valuation
# --------------------------------------------------

def rule_of_40_score(
    revenue_growth,
    fcf_margin
):
    """
    SaaS quality score.

    revenue_growth: % growth (ex: 0.30 for 30%)
    fcf_margin: % margin (ex: 0.15 for 15%)
    """

    score = revenue_growth + fcf_margin

    return score


def rule_of_40_multiple(
    revenue_growth,
    fcf_margin
):
    """
    Estimate EV/revenue multiple based on
    rule of 40 score.
    """

    score = revenue_growth + fcf_margin

    # heuristic scaling
    multiple = score * 0.5

    return multiple


# --------------------------------------------------
# PEG Valuation Model
# --------------------------------------------------

def peg_fair_value(
    eps,
    growth_rate
):
    """
    PEG-based fair price estimate.

    eps: earnings per share
    growth_rate: expected EPS growth (ex: 0.20 for 20%)
    """

    fair_pe = growth_rate * 100

    fair_price = eps * fair_pe

    return fair_price


# --------------------------------------------------
# FCF Yield Valuation
# --------------------------------------------------

def fcf_yield_model(
    free_cash_flow,
    shares_outstanding,
    target_yield=0.04
):
    """
    Values company like a cash flow bond.

    free_cash_flow: annual FCF
    shares_outstanding: total shares
    target_yield: desired yield (default 4%)
    """

    market_cap = free_cash_flow / target_yield

    price = market_cap / shares_outstanding

    return price


# --------------------------------------------------
# Helper Utility
# --------------------------------------------------

def upside_downside(
    fair_value,
    current_price
):
    """
    Calculates percent upside/downside
    """

    if current_price == 0:
        return 0

    return (fair_value / current_price) - 1
