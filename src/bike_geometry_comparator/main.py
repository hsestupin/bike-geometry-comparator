from pathlib import Path

from bike_geometry_comparator.assembly import assemble_all


def main() -> None:
    assemble_all(Path("data"), Path("build/database.csv"))
    # validate("hi")
    print("Bike Geometry Comparator")


if __name__ == "__main__":
    main()
