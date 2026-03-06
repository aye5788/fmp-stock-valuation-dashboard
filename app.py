import streamlit as st

from components.charts import price_chart
from components.fundamentals import fundamentals_charts
from components.valuation_box import valuation_panel

from api.fmp_client import (
    get_financial_growth,
    get_balance_sheet_growth,
    get_cashflow_statement_growth,
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
    # Pull growth datasets
    # --------------------------------------------------

    financial_growth = get_financial_growth(symbol)
    balance_growth = get_balance_sheet_growth(symbol)
    cashflow_growth = get_cashflow_statement_growth(symbol)

    # --------------------------------------------------
    # Growth Metrics
    # --------------------------------------------------

    st.divider()
    st.header("Growth Metrics")

    # ---------------------------
    # Growth Speed
    # ---------------------------

    if not financial_growth.empty:

        financial_growth = financial_growth.sort_values("date")

        st.subheader("Growth Speed")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Revenue Growth",
            f"{financial_growth['revenueGrowth'].iloc[-1]*100:.1f}%"
        )

        col2.metric(
            "EPS Growth",
            f"{financial_growth['epsgrowth'].iloc[-1]*100:.1f}%"
        )

        col3.metric(
            "Operating Income Growth",
            f"{financial_growth['operatingIncomeGrowth'].iloc[-1]*100:.1f}%"
        )

        chart = financial_growth.set_index("date")[["revenueGrowth", "epsgrowth"]]

        st.line_chart(chart)

    else:

        st.info("Financial growth data unavailable")

    # ---------------------------
    # Balance Sheet Quality
    # ---------------------------

    if not balance_growth.empty:

        balance_growth = balance_growth.sort_values("date")

        st.subheader("Balance Sheet Quality")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Receivables Growth",
            f"{balance_growth['growthNetReceivables'].iloc[-1]*100:.1f}%"
        )

        col2.metric(
            "Inventory Growth",
            f"{balance_growth['growthInventory'].iloc[-1]*100:.1f}%"
        )

        col3.metric(
            "Asset Growth",
            f"{balance_growth['growthTotalAssets'].iloc[-1]*100:.1f}%"
        )

        col4.metric(
            "Deferred Revenue Growth",
            f"{balance_growth['growthDeferredRevenue'].iloc[-1]*100:.1f}%"
        )

    else:

        st.info("Balance sheet growth data unavailable")

    # ---------------------------
    # Cash Flow Strength
    # ---------------------------

    if not cashflow_growth.empty:

        cashflow_growth = cashflow_growth.sort_values("date")

        st.subheader("Cash Flow Strength")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Operating Cash Flow Growth",
            f"{cashflow_growth['growthOperatingCashFlow'].iloc[-1]*100:.1f}%"
        )

        col2.metric(
            "Free Cash Flow Growth",
            f"{cashflow_growth['growthFreeCashFlow'].iloc[-1]*100:.1f}%"
        )

        col3.metric(
            "Capex Growth",
            f"{cashflow_growth['growthCapitalExpenditure'].iloc[-1]*100:.1f}%"
        )

        col4.metric(
            "Stock-Based Compensation Growth",
            f"{cashflow_growth['growthStockBasedCompensation'].iloc[-1]*100:.1f}%"
        )

        col5.metric(
            "Net Stock Issuance Growth",
            f"{cashflow_growth['growthNetStockIssuance'].iloc[-1]*100:.1f}%"
        )

    else:

        st.info("Cashflow growth data unavailable")


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
