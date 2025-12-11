import configparser
from pathlib import Path

from bike_geometry_comparator.assembly import assemble_all


def test_canyon():
    do_test("canyon")
    # assert False


def do_test(brand: str) -> None:
    assembled = assemble_all(Path("data"))
    print(f"assembled : {assembled}")
    props = Path("data") / brand / "defaults.ini"
    config = configparser.ConfigParser(allow_unnamed_section=True)
    config.read(props, encoding="utf-8")
    for key, value in config.items(configparser.UNNAMED_SECTION):
        print(f"\n{key}: {value}")
