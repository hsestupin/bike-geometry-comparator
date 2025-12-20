import logging
import shutil
import subprocess
from pathlib import Path

from bike_geometry_comparator.assembly import build_geometry_database
from bike_geometry_comparator.database.core import (
    init_bike_geometry_db,
)
from bike_geometry_comparator.logging.colors import ColorCodes
from bike_geometry_comparator.logging.config import setup_project_root_logging

logger = logging.getLogger(__name__)


def main() -> None:
    setup_project_root_logging(logging.DEBUG)
    build_path = Path("build")
    shutil.rmtree(build_path, ignore_errors=True)
    build_path.mkdir()

    init_bike_geometry_db()
    database_file = build_path / "database.csv"
    build_geometry_database(Path("data"), database_file)
    logger.info(f"{ColorCodes.OKGREEN}Build succesfully finished{ColorCodes.ENDC}. Top 100 rows:")
    subprocess.run(["duckdb", "-c", f"SELECT * FROM '{database_file}' LIMIT 100"])


if __name__ == "__main__":
    main()
