import logging
from importlib.resources import read_text
from typing import Any

import duckdb
from _duckdb import ConstraintException


def init_bike_geometry_db() -> None:
    schema_sql = read_text(__name__, "schema.sql")
    duckdb.sql(schema_sql)


def insert_bike_geometry(select_sql: str) -> None:
    columns = duckdb.execute(f"SELECT column_name FROM (DESCRIBE {select_sql})").fetchall()
    insert_sql = f"""
    INSERT INTO bike_geometry ({", ".join([col for (col,) in columns])}) {select_sql}
    """
    logging.debug("Insert sql: %s", insert_sql)
    try:
        duckdb.sql(insert_sql)
    except ConstraintException as ex:
        ex.add_note(f"Cannot insert bike geometry data: {insert_sql}")
        raise ex


def fetchall_with_columns(conn, sql) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def fetchall_strings(conn, sql) -> list[str]:
    with conn.cursor() as cur:
        return [res for (res,) in cur.execute(sql).fetchall()]
        # columns = [desc[0] for desc in cur.description] if cur.description else []
        # rows = cur.fetchall()
        # return [dict(zip(columns, row)) for row in rows]
