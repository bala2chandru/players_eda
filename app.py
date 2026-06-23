import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Players EDA Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(r"D:\Players\players_cleaned.csv")

df = load_data()

st.title("⚽ Players Performance Analytics Dashboard")

st.sidebar.header("Filters")
team = st.sidebar.selectbox("Select Team", ["All"] + sorted(df["team"].dropna().unique().tolist()))
position = st.sidebar.selectbox("Select Position", ["All"] + sorted(df["position"].dropna().unique().tolist()))

filtered_df = df.copy()
if team != "All":
    filtered_df = filtered_df[filtered_df["team"] == team]
if position != "All":
    filtered_df = filtered_df[filtered_df["position"].astype(str).str.contains(position)]

st.subheader("📊 Dataset Preview")
st.dataframe(filtered_df.head())

st.subheader("📌 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Players", len(filtered_df))
col2.metric("Avg Minutes", round(filtered_df["minutes"].mean(), 2))
col3.metric("Avg Goals", round(filtered_df["goals"].mean(), 2))
col4.metric("Avg Assists", round(filtered_df["assists"].mean(), 2))

st.subheader("⏱ Minutes Distribution")
fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(filtered_df["minutes"], kde=True, ax=ax)
st.pyplot(fig)

st.subheader("🔥 Correlation Heatmap")
num_df = filtered_df.select_dtypes(include="number")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(num_df.corr(), cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.subheader("🎯 Player-Level Insights")
player = st.selectbox("Select Player", sorted(df["player"].dropna().unique().tolist()))
p = df[df["player"] == player].iloc[0]

st.write(f"### {player}")
st.write(f"**Team:** {p['team']}")
st.write(f"**Position:** {p['position']}")
st.write(f"**Minutes Played:** {p['minutes']}")
st.write(f"**Goals:** {p['goals']}")
st.write(f"**Assists:** {p['assists']}")
st.write(f"**Shots:** {p['shots']}")

