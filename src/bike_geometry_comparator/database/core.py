import logging
from importlib.resources import read_text
from typing import Any

from _duckdb import ConstraintException, DuckDBPyConnection

from bike_geometry_comparator.db_utils import fetchall_strings


def init_geometry_database(con: DuckDBPyConnection) -> None:
    schema_sql = read_text(__name__, "schema.sql")
    con.sql(schema_sql)


def insert_bike_geometry(con: DuckDBPyConnection, datasource_query: str) -> None:
    columns = con.execute(f"SELECT column_name FROM (DESCRIBE {datasource_query})").fetchall()
    insert_sql = f"""
    INSERT INTO bike_geometry ({", ".join([col for (col,) in columns])}) {datasource_query}
    """
    logging.debug("Insert sql: %s", insert_sql)
    try:
        con.sql(insert_sql)
    except ConstraintException as ex:
        ex.add_note(f"Cannot insert bike geometry data: {insert_sql}")
        raise ex


def generate_fetch_all_sql_query(con: DuckDBPyConnection) -> str:
    columns_with_artificial_default = fetchall_strings(
        """SELECT column_name
FROM information_schema.columns
WHERE table_name = 'bike_geometry'
 AND column_default == '-1'""",
        con,
    )

    artificial_default_replacements = ",\n".join(
        [
            f"CASE WHEN {column} == -1 THEN NULL ELSE {column} END AS {column}"
            for column in columns_with_artificial_default
        ]
    )
    database_assembly_terminal_query = f"""SELECT * 
REPLACE ({artificial_default_replacements})
FROM bike_geometry"""
    return database_assembly_terminal_query


def fetchall_with_columns(conn, sql) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchall()
        return [dict(zip(columns, row)) for row in rows]
