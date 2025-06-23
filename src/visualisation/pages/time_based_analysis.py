import streamlit as st
import pandas as pd
from src.utils.db_config import get_postgres_connection_url
from sqlalchemy import create_engine
import altair as alt
import sys

conn = create_engine(get_postgres_connection_url())


# --- Step 1: Get list of available years ---
def get_years_months():
    years_query = "SELECT DISTINCT EXTRACT(YEAR FROM crash_date)::INT AS year FROM motor_vehicle_collisions.mvc_crashes_silver ORDER BY year;"
    years_df = pd.read_sql(years_query, conn)
    available_years = years_df["year"].tolist()

    min_year = min(available_years)
    max_year = max(available_years)
    
    month_query = """SELECT DISTINCT EXTRACT(MONTH FROM crash_date)::INT AS month FROM motor_vehicle_collisions.mvc_crashes_silver ORDER BY month;"""
    month_df = pd.read_sql(month_query, conn)
    available_months = month_df["month"].tolist()
    return available_years, min_year, max_year, available_months

available_years, min_year, max_year, available_months = get_years_months()

def show():
    # --- Step 2: User selects year ---
    selected_year = st.selectbox("Select crash year", available_years)
    selected_month = st.selectbox("Select crash month", available_months)

    # --- Step 3: Query with year filter ---
    query = """
    SELECT
        EXTRACT('hour' from crash_time) AS crash_hour,
        SUM(number_of_persons_injured+number_of_persons_killed) AS total_crashes_persons,
        SUM(number_of_pedestrians_injured+number_of_pedestrians_killed) AS total_crashes_pedestrians,
        SUM(number_of_cyclist_injured+number_of_cyclist_killed) AS total_crashes_cyclists,
        SUM(number_of_motorist_injured+number_of_motorist_killed) AS total_crashes_motorists
    FROM motor_vehicle_collisions.mvc_crashes_silver
    WHERE EXTRACT(YEAR FROM crash_date) = %s
    AND EXTRACT(MONTH FROM crash_date) = %s
    GROUP BY 1
    ORDER BY 1;
    """
    df_hourly = pd.read_sql(query, conn, params=(selected_year, selected_month))

    # --- Step 4: Show bar chart ---
    # st.bar_chart(df_hourly.set_index("crash_hour")[["total_injury_persons", "total_injury_pedestrians", "total_injury_cyclists"]])

    query = """
    SELECT
        TRIM(TO_CHAR(crash_date, 'Day')) AS day_of_week,  -- TRIM to remove padding spaces
        SUM(number_of_persons_injured+number_of_persons_killed) AS total_crashes_persons,
        SUM(number_of_pedestrians_injured+number_of_pedestrians_killed) AS total_crashes_pedestrians,
        SUM(number_of_cyclist_injured+number_of_cyclist_killed) AS total_crashes_cyclists,
        SUM(number_of_motorist_injured+number_of_motorist_killed) AS total_crashes_motorists
    FROM motor_vehicle_collisions.mvc_crashes_silver
    WHERE EXTRACT(YEAR FROM crash_date) = %s
    AND EXTRACT(MONTH FROM crash_date) = %s
    GROUP BY 1;
    """

    # Get data
    df_weekly = pd.read_sql(query, conn, params=(selected_year, selected_month))

    # Set correct day order
    day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    df_weekly["day_of_week"] = pd.Categorical(df_weekly["day_of_week"], categories=day_order, ordered=True)
    df_weekly = df_weekly.sort_values("day_of_week")

    # Melt DataFrame to long format for Altair
    df_melted = df_weekly.melt(id_vars="day_of_week", 
                        value_vars=["total_crashes_persons", "total_crashes_pedestrians", "total_crashes_cyclists","total_crashes_motorists"],
                        var_name="injury_type", 
                        value_name="count")

    # Create Altair chart
    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X("day_of_week:N", sort=day_order, title="Day of Week"),
        y=alt.Y("count:Q", title="Injuries"),
        color=alt.Color("injury_type:N", title="Injury Type"),
        tooltip=["day_of_week", "injury_type", "count"]
    ).properties(
        title="Injuries by Day of Week",
        width=700,
        height=400
    )

    # st.altair_chart(chart, use_container_width=True)

    yearly_query = """SELECT
        EXTRACT(YEAR FROM crash_date) as crash_year,
        SUM(number_of_persons_injured+number_of_persons_killed) AS total_crashes_persons,
        SUM(number_of_pedestrians_injured+number_of_pedestrians_killed) AS total_crashes_pedestrians,
        SUM(number_of_cyclist_injured+number_of_cyclist_killed) AS total_crashes_cyclists,
        SUM(number_of_motorist_injured+number_of_motorist_killed) AS total_crashes_motorists
    FROM motor_vehicle_collisions.mvc_crashes_silver
    GROUP BY 1;"""

    df_yearly = pd.read_sql(yearly_query, conn)

    if df_yearly.empty:
        st.error("No data available for the selected year and month.")
    else:
        st.subheader("Hourly Crash Statistics")
        st.bar_chart(df_hourly.set_index("crash_hour")[["total_crashes_persons", "total_crashes_pedestrians", "total_crashes_cyclists","total_crashes_motorists"]])

    if df_weekly.empty:
        st.error("No data available for the selected year and month.")
    else:
        st.subheader("Weekly Crash Statistics")
        st.altair_chart(chart, use_container_width=False)

    st.subheader(f"Yearly Crash Statistics({min_year}-{max_year})")
    st.bar_chart(df_yearly, x="crash_year", y=["total_crashes_persons", "total_crashes_pedestrians", "total_crashes_cyclists","total_crashes_motorists"]
                , stack=False)