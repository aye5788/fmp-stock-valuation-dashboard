import requests
import pandas as pd
import streamlit as st

BASE_URL = "https://financialmodelingprep.com/stable"


def _request(endpoint, params=None):

    if params is None:
        params = {}

    params["apikey"] = st.secrets["FMP_API_KEY"]

    url = f"{BASE_URL}/{endpoint}"

    r = requests.get(url, params=params)

    if r.status_code != 200:
        raise RuntimeError(f"FMP request failed ({r.status_code}): {r.text}")

    return r.json()


# --------------------------------------------------
# Company Profile
# --------------------------------------------------

def get_profile(symbol):

    data = _request(
        "profile",
        {
            "symbol": symbol
        }
    )

    return pd.DataFrame(data)


# --------------------------------------------------
# Quote
# --------------------------------------------------

def get_quote(symbol):

    data = _request(
        "quote",
        {
            "symbol": symbol
        }
    )

    return pd.DataFrame(data)


# --------------------------------------------------
# Income Statement
# --------------------------------------------------

def get_income_statement(symbol, limit=5):

    data = _request(
        "income-statement",
        {
            "symbol": symbol,
            "limit": limit
        }
    )

    return pd.DataFrame(data)


# --------------------------------------------------
# Cash Flow
# --------------------------------------------------

def get_cashflow_statement(symbol, limit=5):

    data = _request(
        "cash-flow-statement",
        {
            "symbol": symbol,
            "limit": limit
        }
    )

    return pd.DataFrame(data)


# --------------------------------------------------
# Balance Sheet
# --------------------------------------------------

def get_balance_sheet(symbol, limit=5):

    data = _request(
        "balance-sheet-statement",
        {
            "symbol": symbol,
            "limit": limit
        }
    )

    return pd.DataFrame(data)


# --------------------------------------------------
# Key Metrics
# --------------------------------------------------

def get_key_metrics(symbol, limit=5):

    data = _request(
        "key-metrics",
        {
            "symbol": symbol,
            "limit": limit
        }
    )

    return pd.DataFrame(data)


# --------------------------------------------------
# PRICE HISTORY (Correct endpoint from docs)
# --------------------------------------------------

def get_price_history(symbol):

    data = _request(
        "historical-price-eod/light",
        {
            "symbol": symbol
        }
    )

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    return df
