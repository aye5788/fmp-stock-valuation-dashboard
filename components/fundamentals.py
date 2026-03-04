import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api.fmp_client import get_income_statement, get_cashflow_statement


def fundamentals_charts(symbol):
    """
    Displays revenue and free cash flow charts.
    """

    income = get_income_statement(symbol)
    cashflow = get_cashflow_statement(symbol)

    if income.empty or cashflow.empty:
        st.warning("Fundamental data unavailable.")
        return

    # Format dates
    income["date"] = pd.to_datetime(income["date"])
    cashflow["date"] = pd.to_datetime(cashflow["date"])

    income = income.sort_values("date")
    cashflow = cashflow.sort_values("date")

    # Revenue chart
    fig_rev = go.Figure()

    fig_rev.add_trace(
        go.Bar(
            x=income["date"],
            y=income["revenue"],
            name="Revenue"
        )
    )

    fig_rev.update_layout(
        title="Revenue",
        template="plotly_white",
        height=300
    )

    st.plotly_chart(fig_rev, use_container_width=True)

    # Free cash flow chart
    fig_fcf = go.Figure()

    fig_fcf.add_trace(
        go.Bar(
            x=cashflow["date"],
            y=cashflow["freeCashFlow"],
            name="Free Cash Flow"
        )
    )

    fig_fcf.update_layout(
        title="Free Cash Flow",
        template="plotly_white",
        height=300
    )

    st.plotly_chart(fig_fcf, use_container_width=True)
