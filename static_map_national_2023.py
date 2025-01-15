import pandas as pd
import pydeck as pdk

# Load the forest fire data
fire_data_path = 'NFDB_large_fires.csv'
df_fires = pd.read_csv(fire_data_path)

# Filter data for the year 2023
df_fires_2023 = df_fires[df_fires['YEAR'] == 2023]

# Create the PyDeck layer for fire points
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_fires_2023,
    get_position='[LONGITUDE, LATITUDE]',
    get_radius=10000,
    get_color=[255, 0, 0],
    pickable=True
)

# Set the viewport for Canada
view_state = pdk.ViewState(
    latitude=df_fires_2023['LATITUDE'].mean(),
    longitude=df_fires_2023['LONGITUDE'].mean(),
    zoom=4,
    pitch=0
)

# Render the deck.gl map
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "Location: {FIRENAME}\nSize: {SIZE_HA} ha"})

# Save the map to an HTML file
html_file_path = "forest_fires_2023_map.html"
r.to_html(html_file_path)




