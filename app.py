import streamlit as st

from components.charts import price_chart
from components.fundamentals import fundamentals_charts
from components.valuation_box import valuation_panel


# --------------------------------------------------
# Page config
# --------------------------------------------------

st.set_page_config(
    page_title="Stock Valuation Dashboard",
    layout="wide"
)

st.title("Stock Valuation Dashboard")


# --------------------------------------------------
# Search bar
# --------------------------------------------------

col_search, col_button = st.columns([3,1])

with col_search:
    ticker_input = st.text_input(
        "Enter Ticker",
        value="",
        placeholder="AAPL, NVDA, SNOW..."
    )

with col_button:
    search_clicked = st.button("Search")


# --------------------------------------------------
# Run dashboard only when button pressed
# --------------------------------------------------

if search_clicked:

    symbol = ticker_input.strip().upper()

    if symbol == "":
        st.warning("Please enter a ticker.")
        st.stop()

    st.divider()

    # --------------------------------------------------
    # Top row
    # --------------------------------------------------

    col_left, col_right = st.columns([1,2])

    with col_left:

        valuation_panel(symbol)

    with col_right:

        price_chart(symbol)

    st.divider()

    # --------------------------------------------------
    # Bottom row
    # --------------------------------------------------

    fundamentals_charts(symbol)
