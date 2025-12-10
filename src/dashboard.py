import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.pipeline import get_clean_data
from src.analytics import (
    compute_summary,
    trips_by_hour,
    top_start_stations,
    top_end_stations,
    busiest_date,
)

st.set_page_config(
    page_title="Toronto Bike-Sharing Dashboard",
    layout="wide",
)

st.title("🚴 Toronto Bike-Sharing Dashboard")
st.write("Sprint 1 & 2: Data pipeline, analytics, and interactive dashboard.")


# ---------- LOAD & FILTER DATA ----------
df = get_clean_data()

# Sidebar filter by user type
if "User Type" in df.columns:
    user_options = ["All"] + sorted(df["User Type"].dropna().unique().tolist())
    selected_type = st.sidebar.selectbox("Filter by User Type", user_options, index=0)

    if selected_type != "All":
        df_filtered = df[df["User Type"] == selected_type].copy()
    else:
        df_filtered = df.copy()
else:
    selected_type = "All"
    df_filtered = df.copy()

summary = compute_summary(df_filtered)


# ---------- KPI CARDS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Trips", f"{summary['total_trips']:,}")

with col2:
    st.metric("Average Duration (min)", summary["avg_duration_min"])

with col3:
    day, count = busiest_date(df_filtered)
    st.metric("Busiest Day", f"{day.date()} ({count} trips)")


st.markdown("---")

# ---------- TRIPS BY HOUR ----------
st.subheader("⏰ Trips by Hour of Day")
by_hour = trips_by_hour(df_filtered)
st.bar_chart(by_hour)
st.caption("Visualizing when bikes are most used during the day (0–23 hours).")

st.markdown("---")

# ---------- TOP STATIONS ----------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏁 Top Start Stations")
    top_start = top_start_stations(df_filtered, n=5)
    st.bar_chart(top_start)

with col_right:
    st.subheader("🏁 Top End Stations")
    top_end = top_end_stations(df_filtered, n=5)
    st.bar_chart(top_end)

st.markdown("---")

# ---------- TRIP DURATION DISTRIBUTION ----------
st.subheader("⏱ Trip Duration Distribution (minutes)")

fig, ax = plt.subplots()
df_filtered["Duration (min)"].clip(upper=180).hist(bins=30, ax=ax)
ax.set_xlabel("Duration (min)")
ax.set_ylabel("Number of trips")
ax.set_title("Trip duration distribution (capped at 180 mins)")
st.pyplot(fig)

# ---------- RAW DATA PREVIEW ----------
with st.expander("🔎 View sample of cleaned data"):
    st.dataframe(df_filtered.head(50))