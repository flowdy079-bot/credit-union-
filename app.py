import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Credit Union Executive Dashboard", layout="wide")

st.title("🏦 Cooperative Credit Union: Executive & Risk Dashboard")
st.markdown("Interactive analytics tracking member growth, liquidity, loan portfolios, and default risks.")

# --- GENERATE SYNTHETIC CREDIT UNION DATA ---
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    data = {
        'member_id': range(1000, 1000 + n),
        'join_year': np.random.choice([2021, 2022, 2023, 2024, 2025], size=n),
        'monthly_savings': np.random.normal(300, 100, n).clip(50, 1200).round(2),
        'active_loan_amount': np.random.exponential(5000, n).clip(0, 25000).round(2),
        'credit_score': np.random.normal(680, 50, n).clip(500, 850).astype(int),
        'risk_category': np.random.choice(['Low Risk', 'Medium Risk', 'High Risk'], size=n, p=[0.65, 0.25, 0.10])
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
selected_risk = st.sidebar.multiselect(
    "Select Risk Category:",
    options=df['risk_category'].unique(),
    default=df['risk_category'].unique()
)

selected_years = st.sidebar.slider(
    "Filter by Member Join Year (Min Year):",
    int(df['join_year'].min()), int(df['join_year'].max()), 2021
)

filtered_df = df[(df['risk_category'].isin(selected_risk)) & (df['join_year'] >= selected_years)]

# --- TOP KPI METRICS ROW ---
st.markdown("### 📊 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Members Tracked", f"{len(filtered_df):,}")
col2.metric("Total Monthly Savings", f"${filtered_df['monthly_savings'].sum():,.2f}")
col3.metric("Total Active Loan Portfolio", f"${filtered_df['active_loan_amount'].sum():,.2f}")
col4.metric("Average Credit Score", f"{int(filtered_df['credit_score'].mean())}")

st.markdown("---")

# --- CHARTS SECTION ---
row_col1, row_col2 = st.columns(2)

with row_col1:
    st.subheader("Loan Distribution by Risk Category")
    fig_risk = px.pie(
        filtered_df, 
        names='risk_category', 
        values='active_loan_amount', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_risk, use_container_width=True)

with row_col2:
    st.subheader("Savings vs. Active Loan Amount")
    fig_scatter = px.scatter(
        filtered_df, 
        x='monthly_savings', 
        y='active_loan_amount', 
        color='risk_category',
        opacity=0.7,
        labels={'monthly_savings': 'Monthly Savings ($)', 'active_loan_amount': 'Active Loan ($)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- DATA TABLE PREVIEW ---
st.subheader("📋 Filtered Member Record Explorer")
st.dataframe(filtered_df[['member_id', 'join_year', 'monthly_savings', 'active_loan_amount', 'credit_score', 'risk_category']], use_container_width=True)
