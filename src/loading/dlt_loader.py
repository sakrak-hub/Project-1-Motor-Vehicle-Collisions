import dlt 
from src.utils.db_config import get_postgres_connection_url
from sqlalchemy import create_engine, text

def drop_raw_tables(table_names):
    engine = create_engine(get_postgres_connection_url())

    query = f"""
    DROP TABLE IF EXISTS motor_vehicle_collisions.{table_names}_raw CASCADE;
    """

    # Explicitly commit after executing DDL
    with engine.begin() as connection:  # This ensures autocommit on success
        connection.execute(text(query))

    print("Raw tables dropped successfully.")


def load_to_postgres(data, name, schema):
    pipeline = dlt.pipeline(destination="postgres", dataset_name=schema)
    load_info = pipeline.run(data, table_name=f"{name}_raw", write_disposition="append")
    print(load_info)
    return load_info