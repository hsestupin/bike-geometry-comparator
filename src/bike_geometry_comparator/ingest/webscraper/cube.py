import csv
import re
from html.parser import HTMLParser
from pathlib import Path


class CubeGeometryHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sizes = []
        self.metrics = {}  # metric_name -> [values]
        self.in_thead = False
        self.in_tbody = False
        self.in_tr = False
        self.in_th = False
        self.in_td = False
        self.current_row = []
        self.current_cell_data = []

    def handle_starttag(self, tag, attrs):
        if tag == "thead":
            self.in_thead = True
        elif tag == "tbody":
            self.in_tbody = True
        elif tag == "tr":
            self.in_tr = True
            self.current_row = []
        elif tag == "th":
            self.in_th = True
            self.current_cell_data = []
        elif tag == "td":
            self.in_td = True
            self.current_cell_data = []

    def handle_endtag(self, tag):
        if tag == "thead":
            self.in_thead = False
        elif tag == "tbody":
            self.in_tbody = False
        elif tag == "tr":
            self.in_tr = False
            if self.in_thead:
                # In Cube HTML, the first element in the header row is an empty <th>,
                # followed by <td> elements for each size.
                self.sizes = [s for s in self.current_row if s.strip()]
            elif self.in_tbody:
                if self.current_row:
                    metric_name = self.clean_metric(self.current_row[0])
                    values = [self.clean_value(metric_name, v) for v in self.current_row[1:]]
                    self.metrics[metric_name] = values
        elif tag == "th":
            self.in_th = False
            self.current_row.append(" ".join(self.current_cell_data).strip())
        elif tag == "td":
            self.in_td = False
            self.current_row.append(" ".join(self.current_cell_data).strip())

    def handle_data(self, data):
        if self.in_th or self.in_td:
            self.current_cell_data.append(data)

    def clean_metric(self, name):
        name = name.lower()
        # Replace spaces and other non-alphanumeric chars with underscores
        name = re.sub(r"[^a-z0-9]", "_", name)
        # Collapse multiple underscores
        name = re.sub(r"_+", "_", name)
        return name.strip("_")

    def clean_value(self, metric_name: str, value: str):
        if metric_name in {
            "top_tube_horizontal",
            "seat_angle",
            "head_tube_angle",
            "bb_height_to_hub",
            "reach",
            "stack",
            "wheelbase",
        }:
            if " / " in value:
                # For some frame geometry values are provded in 2 parts
                # because of the fork SAG
                value_parts = value.split(" / ")
                assert len(value_parts) == 2
                # take 2nd value when fork is not suspended
                value = value_parts[0]

        # Remove "mm" suffix
        value = value.replace("mm", "")
        # Remove "°" suffix
        value = value.replace("°", "")
        # Replace comma with dot for angles/values
        value = value.replace(",", ".")
        return value.strip()


def parse_cube_geometry(html_path: str | Path, csv_path: str | Path):
    html_path = Path(html_path)
    csv_path = Path(csv_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = CubeGeometryHTMLParser()
    parser.feed(html_content)

    if not parser.sizes or not parser.metrics:
        # If we didn't find the expected structure, we might need a more targeted search
        # for the table in the large HTML file.
        pass

    metrics_list = list(parser.metrics.keys())
    header = ["size"] + metrics_list

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(header)

        for i, size in enumerate(parser.sizes):
            row = [_normnalize_size(size)]
            for metric in metrics_list:
                values = parser.metrics[metric]
                if i < len(values):
                    row.append(values[i])
                else:
                    row.append("")
            writer.writerow(row)


def _normnalize_size(size: str) -> str:
    return size.rstrip(" cm")
