import configparser
import logging
from os import listdir
from pathlib import Path
from typing import Any, Dict

import duckdb

from bike_geometry_comparator.database.core import insert_bike_geometry

logger = logging.getLogger(__name__)


def build_geometry_database(data_dir: Path, output_csv: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    sql_queries: list[str] = _assemble_sql_queries(data_dir, {})
    for sql_query in sql_queries:
        insert_bike_geometry(sql_query)

    duckdb.sql("""
    SELECT 
        * EXCLUDE (year), 
        CASE WHEN year == -1 THEN NULL ELSE year END AS year,  
    FROM bike_geometry
    """).write_csv(str(output_csv))


def _assemble_sql_queries(directory: Path, parent_defaults: Dict[str, Any]) -> list[str]:
    defaults_config = directory / "defaults.ini"
    defaults = parent_defaults | _read_defaults(defaults_config) if defaults_config.exists() else {}

    geometry_data = directory / "geometry.csv"
    if geometry_data.exists():
        return [f"(SELECT *, {', '.join([f"'{str(v)}' as {k}" for k, v in defaults.items()])} FROM '{geometry_data}')"]
    else:
        child_queries = []
        for file in listdir(directory):
            child = directory / file
            if child.is_dir():
                child_queries += _assemble_sql_queries(child, defaults)
        return child_queries


def _fetchall_with_columns(conn, sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def _read_defaults(defaults_file: Path) -> Dict[str, Any]:
    config = configparser.ConfigParser(allow_unnamed_section=True)
    config.read(defaults_file, encoding="utf-8")
    return {key: value for key, value in config.items(configparser.UNNAMED_SECTION)}
