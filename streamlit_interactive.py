import pandas as pd
import pydeck as pdk
import streamlit as st
import plotly.express as px

# Load the forest fire data
fire_data_path = 'NFDB_large_fires.csv'
df_fires = pd.read_csv(fire_data_path)

#  Set Streamlit layout and title
st.set_page_config(layout="wide")
st.markdown(f"#### Interactive Forest Fire Map - Canada")
# Dropdown menu for year selection
year_selected = st.selectbox("Select Year", options=list(range(2000, 2024)))

# Filter data to include only fires for the selected year, replace NAN with None
df_fires_selected = df_fires[df_fires['YEAR'] == year_selected].copy()
df_fires_selected = df_fires_selected.where(pd.notnull(df_fires_selected), None)

# Create the PyDeck layer for fire points
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_fires_selected,
    get_position='[LONGITUDE, LATITUDE]',
    get_radius=15000,
    get_color=[255, 0, 0],
    pickable=True
)

# Set the viewport to show all of Canada
view_state = pdk.ViewState(
    latitude=60.0, longitude=-100.0, zoom=2.6, pitch=0
)

# Create the deck.gl map
map_deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-v9",
    tooltip={"text": "Province: {SRC_AGENCY} Date: {MONTH}/{DAY} Size: {SIZE_HA} ha"}
)

# Generate fire counts by province
province_fire_counts_df = df_fires_selected['SRC_AGENCY'].value_counts().reset_index()
province_fire_counts_df.columns = ['SRC_AGENCY', 'Fire Count']

# Plot the bar chart using Plotly
fig = px.bar(
    province_fire_counts_df,
    orientation = 'h',
    x='Fire Count',          # Fire count values
    y='SRC_AGENCY',          # Province codes
    labels={'Fire Count': 'Number of Fires','SRC_AGENCY': 'Province'},
    color_discrete_sequence=['red']  # Set bar color to red
)

# Display map (70%) and bar chart (30%) side by side with custom width
col1, col2 = st.columns([7, 3])  # 70% for map, 30% for chart
with col1:
    st.pydeck_chart(map_deck)
with col2:
    st.plotly_chart(fig, use_container_width=True)

# Display total fire count below the map and chart
total_fire_count = df_fires_selected.shape[0]
st.markdown(f"### Total Fires for the Year {year_selected}: <span style='color:red; font-weight:bold;'>{total_fire_count}</span>", unsafe_allow_html=True)
