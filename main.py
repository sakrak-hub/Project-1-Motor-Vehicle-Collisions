from src.extraction.mvc_extractor import MVCExtractor
from src.loading.dlt_loader import drop_raw_tables
from src.transformation import drop_high_null_count_columns, convert_type_remove_nulls
from src.utils import get_postgres_connection_url
import subprocess
from sqlalchemy import create_engine,text

def check_data_freshness():
    engine = create_engine(get_postgres_connection_url())

    query = """
    SELECT 
	CASE WHEN last_seq_scan IS NULL THEN 0
	ELSE (EXTRACT(epoch FROM (SELECT (NOW() - last_seq_scan)))/86400)::int
	END AS days_since_update
    FROM pg_stat_user_tables
    WHERE relname = 'mvc_crashes_raw';
    """

    with engine.begin() as connection:
        result = connection.execute(text(query))
        row = result.fetchone()
        if row is None or row[0] is None:
            days_since_update =  None
        else:
            days_since_update = row[0]

    if days_since_update is None:
        print("Schema not available. Download to update.", flush=True)
        return True
    elif days_since_update > 7:
        print("More than a week since schema was touched — safe to update.", flush=True)
        return True
    else:
        print(f"Schema was updated {days_since_update} days ago.", flush=True)
        return False

def extract_load_transform():
    mvc_extractor = MVCExtractor()
    for table in mvc_extractor.src_dict.values():
        drop_raw_tables(table)
    mvc_extractor.extract_to_postgres()
    for table in mvc_extractor.src_dict.values():
        drop_high_null_count_columns(table, mvc_extractor.schema)
        convert_type_remove_nulls(f"./sql/transform_{table.split('_')[1]}.sql")

def launch_dashboard():
    subprocess.run(["streamlit", "run", "./src/visualisation/dashboard.py"])

if __name__ == "__main__":
    if check_data_freshness():
        print("Data freshness check passed. Proceeding with extraction, loading, and transformation.", flush=True)
        extract_load_transform()
    launch_dashboard()