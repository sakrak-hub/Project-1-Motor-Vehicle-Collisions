import streamlit as st
import pandas as pd
from src.utils.db_config import get_postgres_connection_url
from sqlalchemy import create_engine
import altair as alt
import sys


conn = create_engine(get_postgres_connection_url())

def show():
    query_injury = """SELECT DISTINCT(v.contributing_factor_1),
    SUM(c.number_of_persons_injured+c.number_of_pedestrians_injured+c.number_of_cyclist_injured+number_of_motorist_injured) as total_injury
    FROM motor_vehicle_collisions.mvc_vehicles_silver v
    LEFT JOIN motor_vehicle_collisions.mvc_crashes_silver c
    ON v.collision_id = c.collision_id
    GROUP BY 1
    HAVING SUM(c.number_of_persons_injured+c.number_of_pedestrians_injured+c.number_of_cyclist_injured+number_of_motorist_injured) IS NOT NULL
    AND v.contributing_factor_1!='Unspecified'
    ORDER BY 2 DESC
    LIMIT 10;"""

    df_injury_contributing_factors = pd.read_sql(query_injury, conn)


    st.title("Top 10 Contributing Factors for Injuries and Death due to Motor Vehicle Collisions in NYC")
    st.subheader("Top 10 Contributing Factors for Injuries Caused by Motor Vehicle Collisions in NYC")
    st.write(df_injury_contributing_factors)
    st.write(alt.Chart(df_injury_contributing_factors).mark_bar().encode(
        x=alt.X("total_injury", title="Total Injuries"),
        y=alt.Y("contributing_factor_1", title="Contributing Factor", sort="-x"),
        color=alt.value("#0000FF")
    ).properties(
        title="Top 10 Contributing Factors for Injuries Caused by Motor Vehicle Collisions in NYC"
    ))


    query_deaths = """SELECT DISTINCT(v.contributing_factor_1),
    SUM(c.number_of_persons_killed+c.number_of_pedestrians_killed+c.number_of_cyclist_killed+number_of_motorist_killed) as total_kills
    FROM motor_vehicle_collisions.mvc_vehicles_silver v
    LEFT JOIN motor_vehicle_collisions.mvc_crashes_silver c
    ON v.collision_id = c.collision_id
    GROUP BY 1
    HAVING SUM(c.number_of_persons_injured+c.number_of_pedestrians_injured+c.number_of_cyclist_injured+number_of_motorist_injured) IS NOT NULL
    AND v.contributing_factor_1!='Unspecified'
    ORDER BY 2 DESC
    LIMIT 10"""

    df_death_contributing_factors = pd.read_sql(query_deaths, conn)

    st.subheader("Top 10 Contributing Factors for Deaths Caused by Motor Vehicle Collisions in NYC")
    st.write(df_death_contributing_factors)
    st.write(alt.Chart(df_death_contributing_factors).mark_bar().encode(
        x=alt.X("total_kills", title="Total Kills"),
        y=alt.Y("contributing_factor_1", title="Contributing Factor", sort="-x"),
        color=alt.value("#FF0000")
    ).properties(
        title="Top 10 Contributing Factors for Deaths Caused by Motor Vehicle Collisions in NYC"
    ))
