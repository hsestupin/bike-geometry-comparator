from pathlib import Path

from bike_geometry_comparator.assembly import build_geometry_database
from bike_geometry_comparator.database.core import init_bike_geometry_db


def test_canyon(tmp_path: Path) -> None:
    do_test("canyon", tmp_path)


def do_test(brand: str, tmp_path: Path) -> None:
    init_bike_geometry_db()
    build_geometry_database(Path("data") / brand, tmp_path / "database.csv")
