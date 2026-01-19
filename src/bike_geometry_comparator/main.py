import logging
import os
import subprocess
from pathlib import Path

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
    subprocess.run(["duckdb", "-c", f"SELECT * FROM '{database_file}' LIMIT 100"])


if __name__ == "__main__":
    main()
