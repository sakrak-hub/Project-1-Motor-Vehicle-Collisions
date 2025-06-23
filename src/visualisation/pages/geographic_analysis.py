import streamlit as st
import pandas as pd
from src.utils.db_config import get_postgres_connection_url
from sqlalchemy import create_engine
import altair as alt
import pydeck as pdk
import plotly.express as px
import json
from .time_based_analysis import get_years_months

conn = create_engine(get_postgres_connection_url())

available_years, min_year, max_year, available_months = get_years_months()

def show():
    selected_year = st.selectbox("Select crash year", available_years)
    selected_month = st.selectbox("Select crash month", available_months)

    borough_query = """SELECT
        borough,
        SUM(number_of_persons_injured) AS total_injury_persons,
        SUM(number_of_pedestrians_injured) AS total_injury_pedestrians,
        SUM(number_of_cyclist_injured) AS total_injury_cyclists
    FROM motor_vehicle_collisions.mvc_crashes_silver
    GROUP BY 1,EXTRACT(YEAR FROM crash_date), EXTRACT(MONTH FROM crash_date)
    HAVING borough != 'Unspecified'
    AND EXTRACT(YEAR FROM crash_date) = %s
    AND EXTRACT(MONTH FROM crash_date) = %s;"""

    df_boroughs = pd.read_sql(borough_query, conn, params=(selected_year,selected_month))

    if df_boroughs.empty:
        st.error("No data available for the selected year and month.")
    else:
        st.subheader(f"Motor Vehicle Collisions by Borough")
        st.bar_chart(df_boroughs,x="borough", y=["total_injury_persons", "total_injury_pedestrians", "total_injury_cyclists"])

    map_query = """
    SELECT borough, 
        SUM(number_of_persons_injured + number_of_pedestrians_injured + number_of_cyclist_injured) AS total_crashes
    FROM motor_vehicle_collisions.mvc_crashes_silver
    WHERE EXTRACT(YEAR FROM crash_date) = %s
    AND EXTRACT(MONTH FROM crash_date) = %s
    AND borough IS NOT NULL
    GROUP BY borough;
    """
    df_map = pd.read_sql(map_query, conn, params=(selected_year, selected_month))
    df_map["borough"] = df_map["borough"].str.title()

    # --- Load GeoJSON ---
    with open("/mnt/d/Projects/Project-1-Motor-Vehicle-Collisions-/src/visualisation/data/Borough Boundaries_20250615.geojson") as f:
        borough_geojson = json.load(f)

    # --- Merge crash data into GeoJSON ---
    for feature in borough_geojson["features"]:
        boroname = feature["properties"]["boroname"].title()
        match = df_map[df_map["borough"] == boroname]
        if not match.empty:
            feature["properties"]["total_crashes"] = int(match["total_crashes"].values[0])
        else:
            feature["properties"]["total_crashes"] = 0  # fill with zero if no data

    max_crashes = max(
        feature["properties"]["total_crashes"] for feature in borough_geojson["features"]
    ) or 1
    
    # --- Render choropleth ---
    if df_map['total_crashes'].sum() == 0:
        st.error("No data available for the selected year and month.")
    else:
        st.subheader(f"Motor Vehicle Collisions by Borough - {selected_year}-{selected_month:02d}")
        st.write("This map shows the total number of motor vehicle collisions in each borough for the selected month and year.")
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=40.7128,
                longitude=-74.0060,
                zoom=10,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "GeoJsonLayer",
                    data=borough_geojson,
                    get_fill_color="""
                        [
                            255,
                            100 * (properties.total_crashes / %d),
                            100 * (properties.total_crashes / %d),
                            180
                        ]
                    """ % (max_crashes, max_crashes),
                    get_line_color=[0, 0, 0],
                    pickable=True,
                    auto_highlight=True,
                )
            ],
            tooltip={"text": "{boroname}\nCrashes: {total_crashes}"}
        ))