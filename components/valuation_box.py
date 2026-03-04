import streamlit as st

from api.fmp_client import (
    get_quote,
    get_income_statement,
    get_cashflow_statement,
    get_balance_sheet
)

from models.valuation_models import (
    revenue_multiple_model,
    peg_fair_value,
    rule_of_40_score,
    rule_of_40_multiple,
    fcf_yield_model,
    upside_downside
)


def valuation_panel(symbol):

    quote = get_quote(symbol)
    income = get_income_statement(symbol)
    cashflow = get_cashflow_statement(symbol)
    balance = get_balance_sheet(symbol)

    if quote.empty or income.empty:
        st.warning("Valuation data unavailable.")
        return

    price = quote.iloc[0]["price"]

    revenue = income.iloc[0]["revenue"]
    eps = income.iloc[0]["eps"]
    shares = income.iloc[0]["weightedAverageShsOut"]

    prev_revenue = income.iloc[1]["revenue"]

    revenue_growth = (revenue / prev_revenue) - 1

    fcf = cashflow.iloc[0]["freeCashFlow"]

    debt = balance.iloc[0]["totalDebt"]
    cash = balance.iloc[0]["cashAndCashEquivalents"]

    net_debt = debt - cash

    fcf_margin = fcf / revenue

    st.header("Valuation Models")

    st.write(f"**Current Price:** ${price:,.2f}")

    st.write("---")

    # Revenue Multiple Model

    multiple = st.slider(
        "EV / Revenue Multiple",
        min_value=1.0,
        max_value=20.0,
        value=8.0
    )

    revenue_price = revenue_multiple_model(
        revenue,
        shares,
        multiple,
        net_debt
    )

    st.metric(
        "Revenue Multiple Value",
        f"${revenue_price:,.2f}",
        f"{upside_downside(revenue_price, price):.1%}"
    )

    st.caption(
        f"Revenue: ${revenue/1e9:.1f}B | Multiple Used: {multiple}x"
    )

    st.write("---")

    # PEG Model

    if revenue_growth <= 0:

        st.metric(
            "PEG Model",
            "Not meaningful",
            "Negative growth"
        )

    else:

        peg_price = peg_fair_value(
            eps,
            revenue_growth
        )

        st.metric(
            "PEG Model Value",
            f"${peg_price:,.2f}",
            f"{upside_downside(peg_price, price):.1%}"
        )

        st.caption(
            f"EPS: {eps:.2f} | Growth: {revenue_growth:.2%}"
        )

    st.write("---")

    # Rule of 40

    score = rule_of_40_score(
        revenue_growth,
        fcf_margin
    )

    st.metric(
        "Rule of 40 Score",
        f"{score:.2f}"
    )

    st.caption(
        f"Revenue Growth: {revenue_growth:.2%} | FCF Margin: {fcf_margin:.2%}"
    )

    st.write("---")

    # FCF Yield Model

    fcf_price = fcf_yield_model(
        fcf,
        shares
    )

    st.metric(
        "FCF Yield Value",
        f"${fcf_price:,.2f}",
        f"{upside_downside(fcf_price, price):.1%}"
    )

    st.caption(
        f"Free Cash Flow: ${fcf/1e9:.1f}B"
    ).2f}")
