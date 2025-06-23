import dlt


def get_postgres_connection_url() -> str:
    """
    Reads Postgres credentials from DLT's secrets.toml and returns a connection URL.
    """
    try:
        creds = dlt.secrets["destination"]["postgres"]["credentials"]

        username = creds["username"]
        password = creds["password"]
        host = creds["host"]
        port = creds["port"]
        database = creds["database"]

        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

    except KeyError as e:
        raise ValueError(f"Missing key in DLT secrets file: {e}")


def get_psycopg2_conn_params() -> dict:
    """
    Returns a psycopg2-compatible dictionary of connection parameters.
    """
    try:
        creds = dlt.secrets["destination"]["postgres"]["credentials"]

        return {
            "dbname": creds["database"],
            "user": creds["username"],
            "password": creds["password"],
            "host": creds["host"],
            "port": creds["port"],
        }

    except KeyError as e:
        raise ValueError(f"Missing key in DLT secrets file: {e}")
