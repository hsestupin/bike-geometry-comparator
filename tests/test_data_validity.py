from pathlib import Path

import duckdb

from bike_geometry_comparator.db_utils import fetchall_strings


def test_canyon_endurace_exists(geometry_database: Path) -> None:
    sizes = fetchall_strings(f"SELECT size FROM '{geometry_database}' WHERE brand = 'Canyon' and model = 'Endurace'")
    assert all(expected in sizes for expected in ["2XS", "XS", "M", "XL"])


def test_canyon_aeroad_exists(geometry_database: Path) -> None:
    sizes = fetchall_strings(f"SELECT size FROM '{geometry_database}' WHERE brand = 'Canyon' and model = 'Aeroad'")
    assert all(expected in sizes for expected in ["2XS", "XS", "M", "XL"])


def test_stack_validity(geometry_database: Path) -> None:
    (min_stack, max_stack) = duckdb.execute(f"SELECT min(stack), max(stack) FROM '{geometry_database}'").fetchone()
    assert min_stack > 300
    assert max_stack < 800


def test_reach_validity(geometry_database: Path) -> None:
    (min_reach, max_reach) = duckdb.execute(f"SELECT min(reach), max(reach) FROM '{geometry_database}'").fetchone()
    assert min_reach > 300
    assert max_reach < 550


def test_no_mock_data(geometry_database: Path) -> None:
    year_mock_values = duckdb.execute(f"SELECT year FROM '{geometry_database}' where year < 0").fetchall()
    assert year_mock_values == []
