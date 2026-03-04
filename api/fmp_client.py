import requests
import pandas as pd
import streamlit as st
from typing import Any, Dict, Optional, Union

BASE_URL = "https://financialmodelingprep.com/stable"


def _get_api_key() -> str:
    try:
        return st.secrets["FMP_API_KEY"]
    except Exception as e:
        raise RuntimeError(
            "Missing FMP_API_KEY. Add it to Streamlit Secrets (Cloud) or "
            "to .streamlit/secrets.toml (local)."
        ) from e


def _request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], list]:
    """
    Calls an FMP Stable endpoint and returns parsed JSON.

    - Uses query param apikey (simple + reliable).
    - Adds a timeout.
    - Returns [] on empty/invalid JSON.
    - Raises a helpful exception on non-200 responses.
    """
    if params is None:
        params = {}

    params = dict(params)
    params["apikey"] = _get_api_key()

    url = f"{BASE_URL}/{endpoint}"

    try:
        r = requests.get(url, params=params, timeout=20)
    except requests.RequestException as e:
        raise RuntimeError(f"Network error calling FMP: {e}") from e

    # Some FMP endpoints may return 200 with [] (meaning "no data"),
    # so we only hard-fail on non-200.
    if r.status_code != 200:
        # keep response text for debugging
        raise RuntimeError(f"FMP request failed ({r.status_code}): {r.text}")

    # Parse JSON safely
    try:
        return r.json()
    except ValueError:
        return []


# -----------------------------
# Stable endpoints (core)
# -----------------------------

def get_profile(symbol: str) -> pd.DataFrame:
    data = _request("profile", {"symbol": symbol})
    # usually list[dict]
    return pd.DataFrame(data if isinstance(data, list) else [])


def get_quote(symbol: str) -> pd.DataFrame:
    data = _request("quote", {"symbol": symbol})
    return pd.DataFrame(data if isinstance(data, list) else [])


def get_income_statement(symbol: str, limit: int = 5) -> pd.DataFrame:
    data = _request("income-statement", {"symbol": symbol, "limit": limit})
    return pd.DataFrame(data if isinstance(data, list) else [])


def get_cashflow_statement(symbol: str, limit: int = 5) -> pd.DataFrame:
    data = _request("cash-flow-statement", {"symbol": symbol, "limit": limit})
    return pd.DataFrame(data if isinstance(data, list) else [])


def get_balance_sheet(symbol: str, limit: int = 5) -> pd.DataFrame:
    data = _request("balance-sheet-statement", {"symbol": symbol, "limit": limit})
    return pd.DataFrame(data if isinstance(data, list) else [])


def get_key_metrics(symbol: str, limit: int = 5) -> pd.DataFrame:
    data = _request("key-metrics", {"symbol": symbol, "limit": limit})
    return pd.DataFrame(data if isinstance(data, list) else [])


# -----------------------------
# Price history (Stable)
# -----------------------------

def get_price_history(symbol: str) -> pd.DataFrame:
    """
    Uses Stable historical price endpoint.

    NOTE:
    Many FMP historical endpoints return an object like:
      {"symbol": "AAPL", "historical": [ ... ]}

    We normalize to a flat DataFrame with columns like date/open/high/low/close/volume.
    """
    # ✅ Stable-style: historical-price-full
    data = _request("historical-price-full", {"symbol": symbol})

    # If API returns [] (no data), return empty df
    if not data:
        return pd.DataFrame()

    # If dict with "historical", extract it
    if isinstance(data, dict) and "historical" in data and isinstance(data["historical"], list):
        df = pd.DataFrame(data["historical"])
        return df

    # If it unexpectedly returns a list, try it directly
    if isinstance(data, list):
        return pd.DataFrame(data)

    return pd.DataFrame()
