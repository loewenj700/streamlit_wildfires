import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Load & clean
# ----------------------------
df = pd.read_csv("NFDB_large_fires.csv")
df.columns = df.columns.str.strip().str.upper()

# Valid coordinates only
df = df[(df["LATITUDE"].notna()) & (df["LONGITUDE"].notna())]
df = df[(df["LATITUDE"] != 0) & (df["LONGITUDE"] != 0)]

# Ensure types
df = df[df["YEAR"].notna()]
df["YEAR"] = df["YEAR"].astype(int)

# 20-year window based on data
max_year = int(df["YEAR"].max())
recent_years = list(range(max_year - 19, max_year + 1))
df_recent = df[df["YEAR"].isin(recent_years)].copy()

# ----------------------------
# App layout
# ----------------------------
st.set_page_config(page_title="Canadian Wildfires – Entry Point Explorer", layout="wide")
st.subheader("🔥 Canadian Wildfires: Entry Point Explorer")

tab1, tab2, tab3 = st.tabs(["📊 Biggest Fire Ever", "🗺️ Top 10 Fires Map", "🧭 Explore by Year"])

# =========================================================
# TAB 1 — Largest Fire Ever
# =========================================================
with tab1:
    st.subheader("Canada's Largest Wildfire on Record:")

    idx_max = df["SIZE_HA"].idxmax()
    largest = df.loc[idx_max]

    largest_size = float(largest["SIZE_HA"])
    largest_year = int(largest["YEAR"])
    largest_id = str(largest["FIRE_ID"]) if "FIRE_ID" in df.columns and pd.notna(largest.get("FIRE_ID")) else "N/A"
    largest_name = str(largest["FIRENAME"]) if "FIRENAME" in df.columns and pd.notna(largest.get("FIRENAME")) else "N/A"

    st.header(f"{largest_size:,.0f} hectares burned 🔥")
    st.write(f"Occurred in **{largest_year}** • Fire ID: `{largest_id}` • Name: `{largest_name}`")

# =========================================================
# TAB 2 — Top 10 Fires Map (BIGGER DOTS, NO LEGEND)
# =========================================================
with tab2:
    st.subheader("Where the 10 Largest Fires Happened")

    top10 = df.sort_values("SIZE_HA", ascending=False).head(10).copy()

    fig = px.scatter_mapbox(
        top10,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="FIRE_ID" if "FIRE_ID" in top10.columns else None,
        hover_data={"SIZE_HA": True, "YEAR": True},
        zoom=3,
        height=620
    )
    # Bigger dots, fixed margins, no legend
    fig.update_traces(marker=dict(size=28, color="red", opacity=0.7))
    fig.update_layout(
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 3 — Explore by Year (BIGGER DOTS, NO LEGEND)
# =========================================================
with tab3:
    st.subheader(f"Explore Wildfires by Year ({recent_years[0]}–{recent_years[-1]})")

    year_selected = st.selectbox("Select a year:", sorted(recent_years, reverse=True))
    df_year = df_recent[df_recent["YEAR"] == year_selected].copy()

    fig2 = px.scatter_mapbox(
        df_year,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="FIRE_ID" if "FIRE_ID" in df_year.columns else None,
        hover_data={"SIZE_HA": True, "CAUSE": True, "YEAR": True},
        zoom=3,
        height=680
    )
    # Bigger dots, fixed margins, no legend
    fig2.update_traces(marker=dict(size=20, color="red", opacity=0.6))
    fig2.update_layout(
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.write(f"Showing **{len(df_year)}** large fires from **{year_selected}**")

