import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api.fmp_client import (
    get_income_statement,
    get_cashflow_statement,
    get_balance_sheet
)


def fundamentals_charts(symbol):

    income = get_income_statement(symbol)
    cashflow = get_cashflow_statement(symbol)
    balance = get_balance_sheet(symbol)

    if income.empty:
        st.warning("No fundamental data available.")
        return

    income["date"] = pd.to_datetime(income["date"])
    cashflow["date"] = pd.to_datetime(cashflow["date"])
    balance["date"] = pd.to_datetime(balance["date"])

    income = income.sort_values("date")
    cashflow = cashflow.sort_values("date")
    balance = balance.sort_values("date")

    # ---------------------------
    # YoY calculations
    # ---------------------------

    income["revenue_yoy"] = income["revenue"].pct_change()
    income["gross_yoy"] = income["grossProfit"].pct_change()
    income["net_yoy"] = income["netIncome"].pct_change()

    cashflow["fcf_yoy"] = cashflow["freeCashFlow"].pct_change()

    st.header("Fundamentals")

    col1, col2 = st.columns(2)

    # Revenue
    with col1:

        fig = go.Figure()

        fig.add_bar(
            x=income["date"],
            y=income["revenue"],
            text=[
                f"{v:.0%}" if pd.notna(v) else ""
                for v in income["revenue_yoy"]
            ],
            textposition="outside"
        )

        fig.update_layout(
            title="Revenue",
            template="plotly_white",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    # Gross Profit
    with col2:

        fig = go.Figure()

        fig.add_bar(
            x=income["date"],
            y=income["grossProfit"],
            text=[
                f"{v:.0%}" if pd.notna(v) else ""
                for v in income["gross_yoy"]
            ],
            textposition="outside"
        )

        fig.update_layout(
            title="Gross Profit",
            template="plotly_white",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    # Net Income
    with col3:

        fig = go.Figure()

        fig.add_bar(
            x=income["date"],
            y=income["netIncome"],
            text=[
                f"{v:.0%}" if pd.notna(v) else ""
                for v in income["net_yoy"]
            ],
            textposition="outside"
        )

        fig.update_layout(
            title="Net Income",
            template="plotly_white",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    # Free Cash Flow
    with col4:

        fig = go.Figure()

        fig.add_bar(
            x=cashflow["date"],
            y=cashflow["freeCashFlow"],
            text=[
                f"{v:.0%}" if pd.notna(v) else ""
                for v in cashflow["fcf_yoy"]
            ],
            textposition="outside"
        )

        fig.update_layout(
            title="Free Cash Flow",
            template="plotly_white",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    col5, col6 = st.columns(2)

    # Operating Margin
    with col5:

        income["operatingMargin"] = income["operatingIncome"] / income["revenue"]

        fig = go.Figure()

        fig.add_scatter(
            x=income["date"],
            y=income["operatingMargin"],
            mode="lines+markers"
        )

        fig.update_layout(
            title="Operating Margin",
            template="plotly_white",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    # Debt vs Cash
    with col6:

        fig = go.Figure()

        fig.add_bar(
            x=balance["date"],
            y=balance["totalDebt"],
            name="Debt"
        )

        fig.add_bar(
            x=balance["date"],
            y=balance["cashAndCashEquivalents"],
            name="Cash"
        )

        fig.update_layout(
            title="Debt vs Cash",
            barmode="group",
            template="plotly_white",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)
