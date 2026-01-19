import argparse
import csv
import re
from pathlib import Path
from typing import Any


def parse_raw_geometry(input_path: str | Path, output_csv_path: str | Path) -> None:
    """
    Parse a raw Trek geometry file and save the data to a CSV file.

    Args:
        input_path: Path to the raw file with geometry data to parse
        output_csv_path: Path to the output CSV file
    """
    input_path = Path(input_path)
    output_csv_path = Path(output_csv_path)

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Parse the file structure
    # First section: header with metric names (tab-indented lines after first line)
    # Then: size blocks where size name is not indented, followed by tab-indented values

    metrics: list[str] = []
    sizes_data: dict[str, dict[str, Any]] = {}
    current_size: str | None = None
    current_values: list[Any] = []

    # First pass: identify structure
    header_section = True
    first_line = True
    metric_idx = 0

    for line in lines:
        stripped = line.rstrip("\n\r")

        if not stripped:
            continue

        is_indented = stripped.startswith("\t")
        content = stripped.lstrip("\t")

        if first_line:
            # First line is "Frame size letter" - skip it
            first_line = False
            continue

        if header_section:
            if is_indented:
                # This is a metric name in the header
                metric_name = _normalize_metric_name(content)
                metrics.append(metric_name)
            else:
                # First non-indented line after header - this is a size
                header_section = False
                current_size = content
                current_values = []
        else:
            if is_indented:
                # This is a value for the current size
                cleaned_value = _clean_value(metrics[metric_idx], content)
                current_values.append(cleaned_value)
                metric_idx += 1
            else:
                metric_idx = 0
                # New size - save previous size data first
                if current_size is not None and current_values:
                    sizes_data[current_size] = dict(zip(metrics, current_values))
                current_size = content
                current_values = []

    # Don't forget the last size
    if current_size is not None and current_values:
        sizes_data[current_size] = dict(zip(metrics, current_values))

    # Write to CSV with size as a column
    output_csv_path.parent.mkdir(exist_ok=True, parents=True)

    headers = ["size"] + metrics

    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        for size, data in sizes_data.items():
            row = {"size": size}
            row.update(data)
            writer.writerow(row)


def _normalize_metric_name(name: str) -> str:
    """
    Normalize metric name to lowercase with underscores.

    - Remove letter prefix like "A — " or "B — "
    - Convert to lowercase
    - Replace spaces with underscores
    """
    # Remove letter prefix pattern like "A — ", "B — ", etc.
    # The em-dash (—) is Unicode character U+2014
    name = re.sub(r"^[A-Z]\s*[—–-]\s*", "", name)

    # Convert to lowercase and replace spaces with underscores
    name = name.lower().replace(" ", "_").replace("(", "_").replace(")", "_").replace("/", "_")

    # Clean up any multiple underscores
    name = re.sub(r"_+", "_", name)
    if name == "offset":
        return "_offset"
    return name


def convert_to_mm(value: str) -> float:
    return float(value) * 10


def _clean_value(metric: str, value: str) -> Any:
    """
    Clean a metric value.

    - Remove "mm" suffix
    - For angles: remove '°' suffix and replace comma with dot
    """
    # Remove mm suffix (case insensitive)
    value = re.sub(r"\s*mm$", "", value, flags=re.IGNORECASE)

    # Handle angle values - remove degree symbol and replace comma with dot
    if "°" in value:
        value = value.replace("°", "").replace(",", ".")

    # Strip any remaining whitespace
    value = value.strip()

    cm_metrics = {
        "seat_tube",
        "head_tube_length",
        "effective_top_tube",
        "bottom_bracket_drop",
        "chainstay_length",
        "offset",
        "trail",
        "wheelbase",
        "standover",
        "frame_reach",
        "frame_stack",
    }
    if metric in cm_metrics:
        return convert_to_mm(value)

    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="TrekIngester",
        description="Parses geometry data copied manually from geometry chart on Trek's site ",
    )
    parser.add_argument("file")
    parser.add_argument("-c", "--csv", help="Output csv file")
    args = parser.parse_args()
    file = Path(args.file)
    csv_arg = args.csv

    build_path = Path("build")
    build_path.mkdir(exist_ok=True)
    out_csv = Path(csv_arg or build_path / "trek_geometry.csv")
    out_csv.parent.mkdir(exist_ok=True, parents=True)
    parse_raw_geometry(file, out_csv)
    print(f"CSV written to: {out_csv}")
