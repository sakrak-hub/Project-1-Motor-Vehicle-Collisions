from src.extraction.mvc_extractor import MVCExtractor
from src.loading.dlt_loader import drop_raw_tables
from src.transformation import drop_high_null_count_columns, convert_type_remove_nulls
import subprocess

def main():
    drop_raw_tables()
    mvc_extractor = MVCExtractor()
    mvc_extractor.extract_to_postgres()
    for table in mvc_extractor.src_dict.values():
        drop_high_null_count_columns(table, mvc_extractor.schema)
        convert_type_remove_nulls(f"./sql/transform_{table.split('_')[1]}.sql")

def launch_dashboard():
    subprocess.run(["streamlit", "run", "./src/visualisation/dashboard.py"])

if __name__ == "__main__":
    main()
    launch_dashboard()