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
# Grading functions
# --------------------------------------------------

def grade_growth(metric, value):

    if metric in ["revenue","eps","operating","ocf","fcf"]:

        if value >= 0.30: return "A"
        if value >= 0.20: return "B"
        if value >= 0.10: return "C"
        if value >= 0.00: return "D"
        return "F"

    if metric == "receivables":

        if value <= 0.15: return "A"
        if value <= 0.30: return "B"
        if value <= 0.50: return "C"
        if value <= 0.80: return "D"
        return "F"

    if metric == "inventory":

        if value <= 0.10: return "A"
        if value <= 0.25: return "B"
        if value <= 0.50: return "C"
        if value <= 1.00: return "D"
        return "F"

    if metric == "assets":

        if value <= 0.10: return "A"
        if value <= 0.20: return "B"
        if value <= 0.40: return "C"
        if value <= 0.60: return "D"
        return "F"

    if metric == "deferred":

        if value >= 0.40: return "A"
        if value >= 0.25: return "B"
        if value >= 0.10: return "C"
        if value >= 0.00: return "D"
        return "F"

    if metric == "capex":

        if value <= 0.10: return "A"
        if value <= 0.25: return "B"
        if value <= 0.50: return "C"
        if value <= 1.00: return "D"
        return "F"

    if metric == "sbc":

        if value <= 0.05: return "A"
        if value <= 0.10: return "B"
        if value <= 0.20: return "C"
        if value <= 0.40: return "D"
        return "F"

    if metric == "issuance":

        if value <= 0.00: return "A"
        if value <= 0.05: return "B"
        if value <= 0.15: return "C"
        if value <= 0.30: return "D"
        return "F"


def grade_color(grade):

    colors = {
        "A":"🟢",
        "B":"🟩",
        "C":"🟡",
        "D":"🟠",
        "F":"🔴"
    }

    return colors.get(grade,"⚪")


def display_metric(col, label, value, metric_type):

    grade = grade_growth(metric_type,value)
    icon = grade_color(grade)

    col.metric(
        label,
        f"{value*100:.1f}%"
    )

    col.markdown(f"**Grade:** {icon} **{grade}**")


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
# Run dashboard
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
    # Fundamentals
    # --------------------------------------------------

    fundamentals_charts(symbol)

    # --------------------------------------------------
    # Pull growth data
    # --------------------------------------------------

    financial_growth = get_financial_growth(symbol)
    balance_growth = get_balance_sheet_growth(symbol)
    cashflow_growth = get_cashflow_statement_growth(symbol)

    # --------------------------------------------------
    # Growth Metrics
    # --------------------------------------------------

    st.divider()
    st.header("Growth Metrics")

    # -------------------
    # Growth Speed
    # -------------------

    if not financial_growth.empty:

        financial_growth = financial_growth.sort_values("date")

        st.subheader("Growth Speed")

        col1,col2,col3 = st.columns(3)

        display_metric(
            col1,
            "Revenue Growth",
            financial_growth["revenueGrowth"].iloc[-1],
            "revenue"
        )

        display_metric(
            col2,
            "EPS Growth",
            financial_growth["epsgrowth"].iloc[-1],
            "eps"
        )

        display_metric(
            col3,
            "Operating Income Growth",
            financial_growth["operatingIncomeGrowth"].iloc[-1],
            "operating"
        )

        chart = financial_growth.set_index("date")[["revenueGrowth","epsgrowth"]]

        st.line_chart(chart)

    # -------------------
    # Balance Sheet Quality
    # -------------------

    if not balance_growth.empty:

        balance_growth = balance_growth.sort_values("date")

        st.subheader("Balance Sheet Quality")

        col1,col2,col3,col4 = st.columns(4)

        display_metric(
            col1,
            "Receivables Growth",
            balance_growth["growthNetReceivables"].iloc[-1],
            "receivables"
        )

        display_metric(
            col2,
            "Inventory Growth",
            balance_growth["growthInventory"].iloc[-1],
            "inventory"
        )

        display_metric(
            col3,
            "Asset Growth",
            balance_growth["growthTotalAssets"].iloc[-1],
            "assets"
        )

        display_metric(
            col4,
            "Deferred Revenue Growth",
            balance_growth["growthDeferredRevenue"].iloc[-1],
            "deferred"
        )

    # -------------------
    # Cash Flow Strength
    # -------------------

    if not cashflow_growth.empty:

        cashflow_growth = cashflow_growth.sort_values("date")

        st.subheader("Cash Flow Strength")

        col1,col2,col3,col4,col5 = st.columns(5)

        display_metric(
            col1,
            "Operating Cash Flow Growth",
            cashflow_growth["growthOperatingCashFlow"].iloc[-1],
            "ocf"
        )

        display_metric(
            col2,
            "Free Cash Flow Growth",
            cashflow_growth["growthFreeCashFlow"].iloc[-1],
            "fcf"
        )

        display_metric(
            col3,
            "Capex Growth",
            cashflow_growth["growthCapitalExpenditure"].iloc[-1],
            "capex"
        )

        display_metric(
            col4,
            "Stock-Based Compensation Growth",
            cashflow_growth["growthStockBasedCompensation"].iloc[-1],
            "sbc"
        )

        display_metric(
            col5,
            "Net Stock Issuance Growth",
            cashflow_growth["growthNetStockIssuance"].iloc[-1],
            "issuance"
        )

    # --------------------------------------------------
    # Revenue Segmentation
    # --------------------------------------------------

    st.divider()
    st.header("Revenue Segmentation")

    col_seg1,col_seg2 = st.columns(2)

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
