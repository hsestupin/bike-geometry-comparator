import logging
from importlib.resources import read_text

import duckdb
from _duckdb import ConstraintException


def init_bike_geometry_db() -> None:
    schema_sql = read_text(__name__, "schema.sql")
    duckdb.sql(schema_sql)


def insert_bike_geometry(select_sql: str) -> None:
    columns = duckdb.execute(
        f"SELECT column_name FROM (DESCRIBE {select_sql})"
    ).fetchall()
    insert_sql = f"""
    INSERT INTO bike_geometry ({", ".join([col for (col,) in columns])}) {select_sql}
    """
    logging.debug("Insert sql: %s", insert_sql)
    try:
        duckdb.sql(insert_sql)
    except ConstraintException as ex:
        ex.add_note(f"Cannot insert bike geometry data: {insert_sql}")
        raise ex
