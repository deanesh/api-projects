# Import required dependencies
import streamlit as st
from utils import StockClient
from datetime import datetime
import traceback

# Initialize the Streamlit app
st.set_page_config(page_title="Stock Market Project", layout="wide")


# Cache the StockClient
@st.cache_resource
def get_stock_client():
    return StockClient()


# Initialize the client
client = get_stock_client()

# Page title and author
st.title(client.TITLE)
st.subheader(client.AUTHOR)

# User input for company name
company = st.text_input("Please enter company name:")
search = None
# If company name is entered
if company:
    try:
        search = client.get_symbols(company)
    except Exception as ex:
        st.error("Error occurred during fetching symbols.")
        st.expander("Error details").write(traceback.format_exc())

    # Check if any results returned
    if search is not None and not search.empty:
        symbols = search["1. symbol"].tolist()

        # Dropdown to select symbol
        selected_symbol = st.selectbox("Select the symbol", options=symbols)

        # Show matching symbol row
        st.dataframe(search[search["1. symbol"] == selected_symbol])

        # Button to plot chart
        if st.button("Plot chart", type="primary"):
            with st.spinner("Fetching data..."):
                df_stock = client.get_daily_data(selected_symbol)

                if df_stock.empty:
                    st.error("No stock data available for selected symbol.")
                else:
                    # Download CSV
                    csv = df_stock.to_csv().encode("utf-8")
                    # Example values
                    company_name = company.replace(
                        " ", "_"
                    )  # Replace spaces with underscores
                    symbol = selected_symbol
                    timestamp = datetime.now().strftime(
                        "%Y-%m-%d_%H-%M-%S"
                    )  # e.g., 2025-09-21_15-45-00

                    # Create filename
                    file_name = f"{company_name}_{symbol}_{timestamp}.csv"

                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=file_name,
                        mime="text/csv",
                    )

                    # Plot candlestick chart
                    fig = client.get_candlestick_chart(df_stock)
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Company does not exist or symbol not found")
else:
    st.info("Please enter a valid company name.")
