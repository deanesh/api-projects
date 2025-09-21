# Import required dependencies
import streamlit as st
from utils import StockClient

# Intialzie the streamlit app
st.set_page_config(page_title="Stock Market Project", layout="wide")


# Get the stock client and caching into temporary memory
@st.cache_resource
def get_stock_client():
    return StockClient()


# initialize the client
client = get_stock_client()

# Add the title to webpage
st.title("Stock Market Project")
st.subheader("Author: Deanesh Takkallapati")

# Take company name as input from user
company = st.text_input("Please enter company name : ")

# If company name is entered show dropdown of symbols
if company:
    search = client.get_symbols(company)
    symbols = search["1. symbol"]
    # Create a dropdown showing different symbols
    selected_symbol = st.selectbox("Select the symbol", options=symbols)
    st.dataframe(search[search["1. symbol"] == selected_symbol])
    # Create a button to plot the chart
    button = st.button("Plot chart", type="primary")
    # If button is pressed plot candlestick chart
    if button:
        with st.spinner("fetching data ..."):
            df_stock = client.get_daily_data(selected_symbol)
            csv = df_stock.to_csv().encode("utf-8")
            st.download_button(
                label="download csv", data=csv, file_name="data.csv", mime="text/csv"
            )
            fig = client.get_candlestick_chart(df_stock)
            st.plotly_chart(fig)
