import argparse
import csv
import re
from pathlib import Path


def _parse_file(input_path: Path, out_csv: Path) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return

    # First line contains sizes
    # Size 51R 51T 54R 54T 56R 56T 58R 58T 61R 61T
    sizes = lines[0].split()[1:]
    num_sizes = len(sizes)

    data: dict[str, dict] = {size: {} for size in sizes}

    mappings = {
        "A": "top_tube_horizontal",
        "B": "seat_tube_length",
        "C": "seat_tube_angle",
        "D": "head_tube_angle",
        "E": "chainstay",
        "F": "fork_rake",
        "G": "wheelbase",
        "H": "trail",
        "I": "bb_drop",
        "J": "front_center_distance",
        "K": "head_tube_length",
        "L": "stack",
        "M": "reach",
        "N": "standover_height",
        "Fork Length - Axle to Crown": "fork_axle_to_crown",
    }

    current_metric = None

    for line in lines[1:]:
        # Identify metric
        metric_match = re.match(r"^([A-N])(\s|$)|^Fork Length - Axle to Crown", line)
        if metric_match:
            if metric_match.group(1):
                letter = metric_match.group(1)
                current_metric = mappings.get(letter)
            else:
                current_metric = "fork_axle_to_crown"

        # Try to extract values from current line
        parts = line.split()
        if len(parts) >= num_sizes:
            # Check the last num_sizes parts
            possible_vals = parts[-num_sizes:]
            if all(re.match(r"^\d+(\.\d+)?$", v) for v in possible_vals):
                # If we are in Trail (H), only take 700x38 as the primary value
                if current_metric == "trail":
                    if "700 x 38" in line:
                        for idx, val in enumerate(possible_vals):
                            data[sizes[idx]]["trail"] = val
                # For other metrics, if we haven't found values yet, take these
                elif current_metric and current_metric not in data[sizes[0]]:
                    for idx, val in enumerate(possible_vals):
                        data[sizes[idx]][current_metric] = val

    headers = ["size"] + list(mappings.values())

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        for size in sizes:
            row = {"size": size}
            row.update({m: data[size].get(m, "") for m in mappings.values()})
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="FairlightIngester",
        description="Parses geometry data copied from Fairlight PDF geometry chart",
    )
    parser.add_argument("file")
    parser.add_argument("-m", "--model", required=True, help="Bike model name")
    parser.add_argument("-c", "--csv", help="Output csv file")
    args = parser.parse_args()
    file = Path(args.file)
    model = args.model
    csv_arg = args.csv

    build_path = Path("build")
    build_path.mkdir(exist_ok=True)
    out_csv = Path(csv_arg or build_path / f"{model}_geometry.csv")
    out_csv.parent.mkdir(exist_ok=True, parents=True)
    _parse_file(file, out_csv)
    print(f"CSV written to: {out_csv}")


if __name__ == "__main__":
    main()
