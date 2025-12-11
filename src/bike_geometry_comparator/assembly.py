import configparser
from os import listdir
from pathlib import Path
from typing import Any, Dict

import duckdb


def assemble_all(data_dir: Path, output_csv: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    sql_queries: list[str] = _assemble_sql_queries(data_dir, {})
    print(f"sql_queries = \n{"\n".join(sql_queries)}")
    export_to_csv_query = f"COPY ({" UNION ALL ".join(sql_queries)}) TO '{output_csv}' (HEADER, DELIMITER ',');"
    print(f"final query = {export_to_csv_query}")
    duckdb.execute(export_to_csv_query)


def _assemble_sql_queries(directory: Path, parent_defaults: Dict[str, Any]) -> list[str]:
    defaults_config = directory / "defaults.ini"
    defaults = parent_defaults | _read_defaults(defaults_config) if defaults_config.exists() else {}

    print(f"merged defaults : {defaults}")
    geometry_data = directory / "geometry.csv"
    if geometry_data.exists():
        res = _fetchall_with_columns(
            duckdb,
            f"(SELECT *, {', '.join([f"'{str(v)}' as {k}" for k, v in defaults.items()])} FROM '{geometry_data}')",
        )
        print("DUCKDB\n")
        print(res)
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
