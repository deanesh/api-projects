# Utility functions for the Streamlit application

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests


class StockClient:
    TITLE = "Stock Market Project"
    AUTHOR = "Author: Deanesh Takkallapati"

    def __init__(self):
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": st.secrets["API_KEY"],
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
        }

    def get_symbols(self, company: str) -> pd.DataFrame:
        querystring = {
            "datatype": "json",
            "keywords": company,
            "function": "SYMBOL_SEARCH",
        }
        response = requests.get(url=self.url, headers=self.headers, params=querystring)
        response.raise_for_status()
        data = response.json()["bestMatches"]
        df_search = pd.DataFrame(data)
        return df_search

    def get_daily_data(self, symbol: str) -> pd.DataFrame:
        querystring = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "datatype": "json",
        }
        response = requests.get(url=self.url, headers=self.headers, params=querystring)
        response.raise_for_status()
        data = response.json()["Time Series (Daily)"]
        df_stock = pd.DataFrame(data).T
        df_stock = df_stock.astype(float).round(2)
        df_stock.index = pd.to_datetime(df_stock.index)
        df_stock.index.name = "Date"
        return df_stock

    def get_candlestick_chart(self, df: pd.DataFrame) -> go.Figure:
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df["1. open"],
                    high=df["2. high"],
                    low=df["3. low"],
                    close=df["4. close"],
                )
            ]
        )
        fig.update_layout(width=1200, height=800)
        return fig
