import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api.fmp_client import get_price_history


def price_chart(symbol):

    df = get_price_history(symbol)

    if df.empty:
        st.warning("No price data available.")
        return

    df = df.sort_values("date")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["price"],
            mode="lines",
            name="Price"
        )
    )

    fig.update_layout(
        title=f"{symbol} Price History",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)
