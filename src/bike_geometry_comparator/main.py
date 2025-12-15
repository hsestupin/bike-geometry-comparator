import logging
import shutil
from pathlib import Path

import duckdb

from bike_geometry_comparator.assembly import build_geometry_database
from bike_geometry_comparator.database.core import (
    init_bike_geometry_db,
)
from bike_geometry_comparator.logging.colors import ColorCodes
from bike_geometry_comparator.logging.config import setup_project_root_logging
from bike_geometry_comparator.logging.pretty import format_table

logger = logging.getLogger(__name__)


def main() -> None:
    setup_project_root_logging()
    build_path = Path("build")
    shutil.rmtree(build_path, ignore_errors=True)
    build_path.mkdir()

    init_bike_geometry_db()
    database_csv = build_path / "database.csv"
    build_geometry_database(Path("data"), database_csv)
    logger.info(f"{ColorCodes.OKGREEN}Build succesfully finished{ColorCodes.ENDC}")

    rows = duckdb.execute(f"SELECT * FROM '{database_csv}' LIMIT 100").fetchall()
    columns = [
        column_name[0] for column_name in duckdb.default_connection().description
    ]
    logger.info(f"Top 100 rows:\n{format_table(rows, columns, 100)}")


if __name__ == "__main__":
    main()
