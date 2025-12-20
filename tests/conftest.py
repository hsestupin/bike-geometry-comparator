from pathlib import Path

import pytest

from bike_geometry_comparator.assembly import assemble_geometry_database


@pytest.fixture(scope="session")
def geometry_database(tmpdir_factory: pytest.TempPathFactory) -> Path:
    database_file = tmpdir_factory.mktemp("test_database") / "database.csv"
    assemble_geometry_database(Path("data"), database_file)
    return database_file
