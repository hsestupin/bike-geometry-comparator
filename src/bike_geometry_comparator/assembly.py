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
    logger.debug(f"Final queries built:\n{'\n'.join(sql_queries)}")
    for sql_query in sql_queries:
        insert_bike_geometry(sql_query)

    duckdb.sql("""
    SELECT * REPLACE (
        CASE WHEN year == -1 THEN NULL ELSE year END AS year
    ), 
    FROM bike_geometry
    """).write_csv(str(output_csv))


def _assemble_sql_queries(directory: Path, parent_defaults: Dict[str, Any]) -> list[str]:
    current_defaults = read_ini(directory / "defaults.ini") or {}
    defaults = parent_defaults | current_defaults

    geometry_data = directory / "geometry.csv"
    if geometry_data.exists():
        metric_mappings: dict[str, str] = read_ini(directory / "metric_mappings.ini") or {}
        metric_list = "*"
        if metric_mappings:
            exclude_list = [k for (k, v) in metric_mappings.items() if v == "-"]
            renamed_metrics = [
                f"{original} as {unified}" for (original, unified) in metric_mappings.items() if unified != "-"
            ]

            exclude_clause = f"EXCLUDE ({', '.join(exclude_list)})" if exclude_list else ""
            rename_clause = f"RENAME ({', '.join(renamed_metrics)})" if renamed_metrics else ""
            metric_list = f"* {exclude_clause} {rename_clause}"
        return [
            f"(SELECT {metric_list}, {', '.join([f"'{str(v)}' as {k}" for k, v in defaults.items()])} FROM '{geometry_data}')"
        ]
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


def read_ini(file: Path) -> dict[str, str] | None:
    if not file.exists():
        return None
    config = configparser.ConfigParser(allow_unnamed_section=True)
    config.read(file, encoding="utf-8")
    return {key: value for key, value in config.items(configparser.UNNAMED_SECTION)}
