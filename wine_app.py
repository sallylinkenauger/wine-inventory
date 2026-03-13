import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Wine Inventory", page_icon="🍷", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    .main { background-color: #1a0a0a; }
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #c9a84c !important; }
    .stApp { background-color: #1a0a0a; color: #f0e6d3; }
    .metric-card { background: linear-gradient(135deg, #2d1515, #1a0a0a); border: 1px solid #c9a84c44; border-radius: 8px; padding: 1.2rem 1.5rem; text-align: center; }
    .metric-label { font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase; color: #c9a84c; margin-bottom: 0.3rem; }
    .metric-value { font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; color: #f0e6d3; line-height: 1; }
    div[data-testid="stDataFrame"] { border: 1px solid #c9a84c33; border-radius: 8px; }
    .stTextInput input, .stNumberInput input, .stSelectbox select { background-color: #2d1515 !important; color: #f0e6d3 !important; border: 1px solid #c9a84c66 !important; border-radius: 6px !important; }
    .stButton > button { background: linear-gradient(135deg, #8b1a1a, #c9a84c); color: white; border: none; border-radius: 6px; font-family: 'Montserrat', sans-serif; font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.5rem 1.5rem; width: 100%; }
    .stButton > button:hover { opacity: 0.88; }
    .stSuccess { background-color: #1a2d1a !important; border-left: 3px solid #4caf50 !important; }
    .stError   { background-color: #2d1a1a !important; border-left: 3px solid #c9a
