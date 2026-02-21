import logging
import os
from pathlib import Path

import duckdb
from rich.console import Console
from rich.table import Table

from bike_geometry_comparator.assembly import assemble_geometry_database
from bike_geometry_comparator.logging.colors import ColorCodes
from bike_geometry_comparator.logging.config import setup_project_root_logging

logger = logging.getLogger(__name__)


def main() -> None:
    setup_project_root_logging(logging.DEBUG)
    build_path = Path("build")
    database_file = build_path / "database.csv"
    if database_file.exists():
        os.remove(database_file)
    build_path.mkdir(exist_ok=True)

    data_dir = Path("data")
    assemble_geometry_database(data_dir, database_file)
    logger.info(f"{ColorCodes.OKGREEN}Build succesfully finished{ColorCodes.ENDC}. Top 100 rows:")

    con = duckdb.connect()
    res = con.query(f"SELECT * FROM '{database_file}' LIMIT 25")
    rows = res.fetchall()
    columns = res.columns

    table = Table(show_header=True)
    for col in columns:
        table.add_column(col)

    for row in rows:
        table.add_row(*[str(item) if item is not None else "" for item in row])

    console = Console()
    console.print(table)


if __name__ == "__main__":
    main()
