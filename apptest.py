import streamlit as st
import pandas as pd

# Sets the page configuration
# You can set the page title and layout here
# Section 2.2
st.set_page_config(page_title="HDB Resale Dashboard", layout="wide")

st.title("Singapore HDB Resale Dashboard")
st.caption("Code-along: building a usable dashboard from real resale transactions.")

st.header("Dashboard Overview")
st.subheader("What this app will show")
st.markdown("""
- Transaction volume after filtering
- Average resale price
- Median floor area
- Town and flat type trends
""")


## 3.1 Load directly first (no caching yet)
DATA_PATH = "./my-streamlit-app/data/resale_data.csv"

df = pd.read_csv(DATA_PATH)
# Lesson assumption:
# this dataset has already gone through EDA and basic cleaning.
# Here we focus on dashboard building, not data cleaning.
# We still set the datetime dtype explicitly for reliable filtering and charting.
df["month"] = pd.to_datetime(df["month"])


## 3.2 First data display
st.write(f"Rows loaded: {len(df):,} | Columns: {len(df.columns)}")
st.dataframe(df.head(20), use_container_width=True)


## 4.1 Sidebar controls
st.sidebar.header("Filters")

# Get unique values for towns and flat types
unique_towns = sorted(df["town"].dropna().unique())
unique_flat_types = sorted(df["flat_type"].dropna().unique())

# Create multi-selects
selected_towns = st.sidebar.multiselect("Town", unique_towns, default=[])
selected_flat_types = st.sidebar.multiselect("Flat Type", unique_flat_types, default=[])


# Create slider for resale price range
min_price = int(df["resale_price"].min())
max_price = int(df["resale_price"].max())
price_range = st.sidebar.slider(
    "Resale Price Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=10000,
)


# Create date input for month range
date_min = df["month"].min().date()
date_max = df["month"].max().date()
date_range = st.sidebar.date_input("Month Range", value=(date_min, date_max))