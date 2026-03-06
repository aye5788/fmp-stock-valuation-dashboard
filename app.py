import streamlit as st

from components.charts import price_chart
from components.fundamentals import fundamentals_charts
from components.valuation_box import valuation_panel

# NEW IMPORTS
from api.fmp_client import (
    get_financial_growth,
    get_revenue_product_segmentation,
    get_revenue_geographic_segmentation
)


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

    # --------------------------------------------------
    # Growth Metrics Section
    # --------------------------------------------------

    st.divider()
    st.header("Growth Metrics")

    growth = get_financial_growth(symbol)

    if not growth.empty:

        growth = growth.sort_values("date")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Revenue Growth",
            f"{growth['revenueGrowth'].iloc[-1]*100:.1f}%"
        )

        col2.metric(
            "EPS Growth",
            f"{growth['epsgrowth'].iloc[-1]*100:.1f}%"
        )

        col3.metric(
            "Operating Income Growth",
            f"{growth['operatingIncomeGrowth'].iloc[-1]*100:.1f}%"
        )

        chart = growth.set_index("date")[["revenueGrowth", "epsgrowth"]]

        st.line_chart(chart)

    else:

        st.info("Growth data not available.")


    # --------------------------------------------------
    # Revenue Segmentation
    # --------------------------------------------------

    st.divider()
    st.header("Revenue Segmentation")

    col_seg1, col_seg2 = st.columns(2)

    with col_seg1:

        product = get_revenue_product_segmentation(symbol)

        if not product.empty:

            st.subheader("Revenue by Product")

            st.bar_chart(
                product.set_index("segment")
            )

        else:

            st.info("Product segmentation not available.")


    with col_seg2:

        geo = get_revenue_geographic_segmentation(symbol)

        if not geo.empty:

            st.subheader("Revenue by Geography")

            st.bar_chart(
                geo.set_index("region")
            )

        else:

            st.info("Geographic segmentation not available.")
