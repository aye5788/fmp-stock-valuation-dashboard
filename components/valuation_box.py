import streamlit as st

from api.fmp_client import (
    get_quote,
    get_income_statement,
    get_cashflow_statement,
    get_balance_sheet
)

from models.valuation_models import (
    revenue_multiple_model,
    rule_of_40_score,
    rule_of_40_multiple,
    peg_fair_value,
    fcf_yield_model,
    upside_downside
)


def valuation_panel(symbol):

    quote = get_quote(symbol)
    income = get_income_statement(symbol)
    cashflow = get_cashflow_statement(symbol)
    balance = get_balance_sheet(symbol)

    if quote.empty:
        st.warning("No quote data.")
        return

    current_price = quote.iloc[0]["price"]

    st.subheader("Valuation Models")

    # --------------------------------------------------
    # Pull inputs
    # --------------------------------------------------

    try:
        revenue = income.iloc[0]["revenue"]
        eps = income.iloc[0]["eps"]

        shares = income.iloc[0]["weightedAverageShsOut"]

        prev_revenue = income.iloc[1]["revenue"]
        revenue_growth = (revenue / prev_revenue) - 1

        free_cash_flow = cashflow.iloc[0]["freeCashFlow"]

        debt = balance.iloc[0]["totalDebt"]
        cash = balance.iloc[0]["cashAndCashEquivalents"]

        net_debt = debt - cash

        fcf_margin = free_cash_flow / revenue

    except Exception as e:

        st.error("Unable to compute valuation inputs.")
        return

    # --------------------------------------------------
    # Revenue multiple valuation
    # --------------------------------------------------

    ev_multiple = st.slider(
        "EV / Revenue Multiple",
        min_value=1.0,
        max_value=20.0,
        value=8.0
    )

    revenue_price = revenue_multiple_model(
        revenue,
        shares,
        ev_multiple,
        net_debt
    )

    # --------------------------------------------------
    # Rule of 40
    # --------------------------------------------------

    rule40 = rule_of_40_score(
        revenue_growth,
        fcf_margin
    )

    rule40_multiple = rule_of_40_multiple(
        revenue_growth,
        fcf_margin
    )

    rule40_price = revenue_multiple_model(
        revenue,
        shares,
        rule40_multiple,
        net_debt
    )

    # --------------------------------------------------
    # PEG valuation
    # --------------------------------------------------

    peg_price = peg_fair_value(
        eps,
        revenue_growth
    )

    # --------------------------------------------------
    # FCF yield valuation
    # --------------------------------------------------

    fcf_price = fcf_yield_model(
        free_cash_flow,
        shares
    )

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------

    st.markdown(f"**Current Price:** ${current_price:,.2f}")

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Revenue Multiple Value",
            f"${revenue_price:,.2f}",
            f"{upside_downside(revenue_price, current_price):.1%}"
        )

        st.metric(
            "Rule of 40 Value",
            f"${rule40_price:,.2f}",
            f"{upside_downside(rule40_price, current_price):.1%}"
        )

    with col2:

        st.metric(
            "PEG Model Value",
            f"${peg_price:,.2f}",
            f"{upside_downside(peg_price, current_price):.1%}"
        )

        st.metric(
            "FCF Yield Value",
            f"${fcf_price:,.2f}",
            f"{upside_downside(fcf_price, current_price):.1%}"
        )

    st.write("")

    st.write(f"**Rule of 40 Score:** {rule40:.2f}")
