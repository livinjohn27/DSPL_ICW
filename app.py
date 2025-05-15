import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/livinjohn27/DSPL_ICW/refs/heads/main/Final_Food_Prices.csv")

df = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "App Description",
    "Average Price Over Time",
    "Price Distribution",
    "Regional Price Differences",
    "Top/Bottom Priced Commodities",
    "Price Volatility",
    "Category-wise Trends",
    "Median vs Mean Comparison"
])

# Description Page
if page == "App Description":
    st.title("📈 Food Price Analysis Dashboard")
    st.markdown("""
        This dashboard is designed for government officials to:

        - Track average and volatile food prices.
        - Compare price changes across commodities and regions.
        - Make informed policy decisions using clear visual insights.

        Data includes commodity-wise pricing, geographic location, and time references.
    """)

# Chart placeholders for further development
elif page == "Average Price Over Time":
    st.title("📊 Average Price Over Time")
    df['Reference_Period_Start'] = pd.to_datetime(df['Reference_Period_Start'])
    avg_price = df.groupby(['Reference_Period_Start', 'Commodity_Name'])['Standardized_Price'].mean().reset_index()

    selected_commodity = st.selectbox("Select a Commodity", df['Commodity_Name'].unique())
    filtered = avg_price[avg_price['Commodity_Name'] == selected_commodity]

    fig = px.line(filtered, x='Reference_Period_Start', y='Standardized_Price',
              title=f'Average Price Over Time: {selected_commodity}')
    st.plotly_chart(fig, use_container_width=True)


elif page == "Price Distribution":
    st.title("📊 Price Distribution by Commodity")
    selected_commodities = st.multiselect("Select Commodities", df['Commodity_Name'].unique(), default=df['Commodity_Name'].unique()[:5])
    filtered = df[df['Commodity_Name'].isin(selected_commodities)]

    fig = px.box(filtered, x='Commodity_Name', y='Standardized_Price',
                title='Price Distribution by Commodity')
    st.plotly_chart(fig, use_container_width=True)


elif page == "Regional Price Differences":
    st.title("🗺️ Regional Price Differences")
    avg_location_price = df.groupby(['Market_Name', 'Latitude', 'Longitude'])['Standardized_Price'].mean().reset_index()

    fig = px.scatter_mapbox(avg_location_price,
                            lat='Latitude', lon='Longitude', size='Standardized_Price',
                            color='Standardized_Price', hover_name='Market_Name',
                            zoom=6, mapbox_style='carto-positron',
                            title='Regional Price Differences')
    st.plotly_chart(fig, use_container_width=True)


elif page == "Top/Bottom Priced Commodities":
    st.title("🏆 Top/Bottom Priced Commodities")
    avg_prices = df.groupby('Commodity_Name')['Standardized_Price'].mean().reset_index()
    top_n = st.slider("Top N Commodities", 5, 20, 10)

    top = avg_prices.sort_values(by='Standardized_Price', ascending=False).head(top_n)
    bottom = avg_prices.sort_values(by='Standardized_Price', ascending=True).head(top_n)

    st.subheader("Top Priced Commodities")
    st.plotly_chart(px.bar(top, x='Commodity_Name', y='Standardized_Price'), use_container_width=True)

    st.subheader("Lowest Priced Commodities")
    st.plotly_chart(px.bar(bottom, x='Commodity_Name', y='Standardized_Price'), use_container_width=True)


elif page == "Price Volatility":
    st.title("📉 Price Volatility")
    volatility = df.groupby('Commodity_Name')['Price_Std'].mean().reset_index()
    volatility = volatility.sort_values(by='Price_Std', ascending=False)

    fig = px.bar(volatility.head(15), x='Commodity_Name', y='Price_Std',
                 title='Most Volatile Commodities (Top 15)')
    st.plotly_chart(fig, use_container_width=True)


elif page == "Category-wise Trends":
    st.title("📂 Category-wise Price Trends")
    df['Reference_Period_Start'] = pd.to_datetime(df['Reference_Period_Start'])
    category_trend = df.groupby(['Reference_Period_Start', 'Commodity_Category'])['Standardized_Price'].mean().reset_index()

    fig = px.line(category_trend, x='Reference_Period_Start', y='Standardized_Price',
                  color='Commodity_Category', title='Category-wise Price Trends')
    st.plotly_chart(fig, use_container_width=True)


elif page == "Median vs Mean Comparison":
    st.title("⚖️ Median vs Mean Price Comparison")
    summary = df.groupby('Commodity_Name')[['Price_Mean', 'Price_Median']].mean().reset_index()

    fig = px.scatter(summary, x='Price_Mean', y='Price_Median',
                     hover_name='Commodity_Name', trendline='ols',
                     title='Median vs Mean Price by Commodity')
    st.plotly_chart(fig, use_container_width=True)

