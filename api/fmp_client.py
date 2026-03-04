import requests
import pandas as pd
import streamlit as st

BASE_URL = "https://financialmodelingprep.com/stable"


def _request(endpoint, params=None):
    """
    Internal helper to call the FMP API and return JSON safely.
    """

    if params is None:
        params = {}

    params["apikey"] = st.secrets["FMP_API_KEY"]

    url = f"{BASE_URL}/{endpoint}"

    r = requests.get(url, params=params)

    if r.status_code != 200:
        raise Exception(f"FMP request failed: {r.text}")

    return r.json()


def get_profile(symbol):
    data = _request("profile", {"symbol": symbol})
    return pd.DataFrame(data)


def get_quote(symbol):
    data = _request("quote", {"symbol": symbol})
    return pd.DataFrame(data)


def get_income_statement(symbol, limit=5):
    data = _request(
        "income-statement",
        {
            "symbol": symbol,
            "limit": limit
        },
    )
    return pd.DataFrame(data)


def get_cashflow_statement(symbol, limit=5):
    data = _request(
        "cash-flow-statement",
        {
            "symbol": symbol,
            "limit": limit
        },
    )
    return pd.DataFrame(data)


def get_balance_sheet(symbol, limit=5):
    data = _request(
        "balance-sheet-statement",
        {
            "symbol": symbol,
            "limit": limit
        },
    )
    return pd.DataFrame(data)


def get_key_metrics(symbol, limit=5):
    data = _request(
        "key-metrics",
        {
            "symbol": symbol,
            "limit": limit
        },
    )
    return pd.DataFrame(data)


def get_price_history(symbol):
    data = _request(
        "historical-price-full",
        {
            "symbol": symbol
        },
    )

    df = pd.DataFrame(data["historical"])
    return df
