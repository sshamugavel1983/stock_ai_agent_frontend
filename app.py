import os
import streamlit as st
import requests

# Set page config with improved aesthetics
st.set_page_config(page_title="Stock AI Agent", layout="centered")

# Custom CSS for better design
st.markdown("""
    <style>
        .title {
            font-size: 36px !important;
            font-weight: bold;
            text-align: center;
        }
        .stButton > button {
            border-radius: 8px;
            border: 2px solid #ff4b4b;
            background-color: white;
            color: #ff4b4b;
            padding: 8px 16px;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #ff4b4b;
            color: white;
        }
        .result-box {
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }
        .news-box {
            background-color: #f3f3f3;
            padding: 15px;
            border-radius: 8px;
            font-size: 16px;
        }
        .news-title {
            font-size: 22px;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown('<p class="title">📊 Stock AI Agent</p>', unsafe_allow_html=True)

# User Input for Stock Ticker
ticker = st.text_input("🔍 Enter stock ticker (e.g., AAPL)", max_chars=10)

# Function to fetch stock prediction
def get_stock_prediction(ticker):
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    response = requests.get(f"{backend_url}/predict?ticker={ticker}")
    if response.status_code == 200:
        return response.json().get("predicted_price", "N/A")
    return "Error fetching prediction."

# Function to fetch stock news sentiment
def get_stock_news_sentiment(ticker):
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    response = requests.get(f"{backend_url}/analyze?ticker={ticker}&question=What is the sentiment?")
    if response.status_code == 200:
        return response.json().get("analysis", "No sentiment data available.")
    return "Error fetching sentiment analysis."

# Layout: Stock Prediction & Sentiment Analysis
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🔮 Predict Stock Price"):
        if ticker:
            predicted_price = get_stock_prediction(ticker)
            st.markdown(f'<p class="result-box">Predicted Price for {ticker}: <span style="color: #2e7d32;">${predicted_price:.2f}</span></p>', unsafe_allow_html=True)

with col2:
    if ticker:
        st.markdown('<p class="news-title">📰 Latest News Sentiment</p>', unsafe_allow_html=True)
        sentiment = get_stock_news_sentiment(ticker)
        st.markdown(f'<p class="news-box">{sentiment}</p>', unsafe_allow_html=True)
