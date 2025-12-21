import configparser
import logging
from os import listdir
from pathlib import Path
from typing import Any

import duckdb
from _duckdb import DuckDBPyConnection

import bike_geometry_comparator.database.core as geometry_db

logger = logging.getLogger(__name__)


def _generate_datasource_queries(
    directory: Path, parent_defaults: dict[str, Any], parent_mappings: dict[str, str]
) -> list[str]:
    metric_defaults = parent_defaults | (read_ini(directory / "defaults.ini") or {})
    metric_mappings = parent_mappings | (read_ini(directory / "metric_mappings.ini") or {})

    geometry_data = directory / "geometry.csv"
    if geometry_data.exists():
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
            f"(SELECT {metric_list}, {', '.join([f"'{str(v)}' as {k}" for k, v in metric_defaults.items()])} FROM '{geometry_data}')"
        ]
    else:
        child_queries = []
        for file in listdir(directory):
            child = directory / file
            if child.is_dir():
                child_queries += _generate_datasource_queries(child, metric_defaults, metric_mappings)
        return child_queries


def read_ini(file: Path) -> dict[str, str] | None:
    if not file.exists():
        return None
    config = configparser.ConfigParser(allow_unnamed_section=True)
    config.read(file, encoding="utf-8")
    return {key: value for key, value in config.items(configparser.UNNAMED_SECTION)}


def assemble_geometry_database(input_dir: Path, output_file: Path):
    with duckdb.connect() as con:
        assembler = _DatabaseFileAssembler(con, input_dir, output_file)
        assembler.assemble()


class _DatabaseFileAssembler:
    def __init__(self, con: DuckDBPyConnection, input_dir: Path, output_file: Path) -> None:
        self._con = con
        self._input_dir = input_dir
        self._output_file = output_file

    def assemble(self):
        geometry_db.init_geometry_database(self._con)
        self._populate_geometry_database()

    def _populate_geometry_database(self) -> None:
        datasource_queries: list[str] = _generate_datasource_queries(self._input_dir, {}, {})
        logger.debug(f"Terminal queries per datasource:\n{'\n'.join(datasource_queries)}")
        for datasource_query in datasource_queries:
            geometry_db.insert_bike_geometry(self._con, datasource_query)

        database_assembly_terminal_query = geometry_db.generate_fetch_all_sql_query(self._con)
        logger.debug(f"Terminal query to assemble database:\n{database_assembly_terminal_query}")
        self._con.sql(database_assembly_terminal_query).write_csv(str(self._output_file))
