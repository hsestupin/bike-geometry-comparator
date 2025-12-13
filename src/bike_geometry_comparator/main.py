from pathlib import Path

from bike_geometry_comparator.assembly import build_geometry_database


def main() -> None:
    build_geometry_database(Path("data"), Path("build/database.csv"))
    # validate("hi")
    print("Bike Geometry Comparator")


if __name__ == "__main__":
    main()
