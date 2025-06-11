import pandas as pd
from sqlalchemy import create_engine,text
import psycopg2
from utils.db_config import get_postgres_connection_url

engine = create_engine(get_postgres_connection_url())

schema = "motor_vehicle_collisions"
table_list = ["mvc_crashes", "mvc_persons", "mvc_vehicles"]

def drop_high_null_count_columns(table_name: str, threshold: float = 0.5):
    null_count_query = f"""
    SELECT key AS column, COUNT(*) AS null_values
    FROM {schema}.{table_name}_raw t
    CROSS JOIN jsonb_each_text(to_jsonb(t))
    WHERE value IS NULL
    GROUP BY key
    ORDER BY null_values DESC;
    """
    
    null_df = pd.read_sql(null_count_query, engine)
    total_rows = pd.read_sql(f"SELECT COUNT(*) FROM {schema}.{table_name}_raw", engine).iloc[0, 0]
    null_df["null_pct"] = null_df["null_values"] / total_rows
    drop_columns = null_df[null_df["null_pct"] > threshold]["column"].tolist()

    chunk_size = 10000
    chunks = pd.read_sql(f"SELECT * FROM {schema}.{table_name}_raw", engine, chunksize=chunk_size)
    temp_table_name = f"temp_transform_{table_name.split('_')[1]}_silver"
    #temp_transform_vehicles_silver
    
    for i, chunk in enumerate(chunks):
        # Drop columns with >80% nulls
        print(f"Processing chunk for {table_name}:", i)
        clean_chunk = chunk.drop(columns=drop_columns)
        clean_chunk.to_sql(
            temp_table_name,
            engine,
            schema="motor_vehicle_collisions",
            if_exists="append" if i > 0 else "replace",
            index=False
        )
        
def convert_type_remove_nulls(sql_file: str):
    with engine.begin() as conn:  # begins transaction
        with open(sql_file) as f:
            statement = ""
            for line in f:
                statement += line
                if ";" in line:
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        print(f"Error: {e}")
                    statement = ""


for table in table_list:
    drop_high_null_count_columns(table)
    sql_name = f"transform_{table.split('_')[1]}.sql"
    convert_type_remove_nulls(f"/mnt/d/Projects/Project-1-Motor-Vehicle-Collisions-/sql/{sql_name}")