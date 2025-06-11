import dlt 

def load_to_postgres(data, name):
    pipeline = dlt.pipeline(destination="postgres", dataset_name="motor_vehicle_collisions")
    load_info = pipeline.run(data, table_name=name, write_disposition="append")
    print(load_info)
    return load_info