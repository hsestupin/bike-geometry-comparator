import csv
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
import ssl


class ScottGeometryURLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.geometry_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            attrs_dict = dict(attrs)
            if attrs_dict.get("id") == "geometry-table":
                self.geometry_url = attrs_dict.get("data-geometry-data-url")


class ScottGeometryTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sizes = []
        self.metrics = {}  # metric_name -> [values]
        self.current_row = []
        self.current_cell_data = []
        self.in_tr = False
        self.in_td = False
        self.in_th = False
        self.is_first_row = True

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_tr = True
            self.current_row = []
        elif tag == "th":
            self.in_th = True
            self.current_cell_data = []
        elif tag == "td":
            self.in_td = True
            self.current_cell_data = []

    def handle_endtag(self, tag):
        if tag == "tr":
            self.in_tr = False
            if self.is_first_row:
                # First row contains sizes
                # According to my inspection, it has empty <th> at the beginning
                self.sizes = [s for s in self.current_row if s.strip()]
                self.is_first_row = False
            else:
                if len(self.current_row) >= 2:
                    # Column 0: A, B, C...
                    # Column 1: metric name
                    # Columns 4, 6, 8... (indices 4, 6, 8, 10, 12, 14, 16): values for XXS/47, XS/49, S/52, M/54, L/56, XL/58, XXL/61
                    metric_name = self.clean_metric(self.current_row[1])

                    # We need to map values to sizes.
                    # In the HTML I saw, there are 18 columns in total for the first row.
                    # Column indices with sizes: 4, 6, 8, 10, 12, 14, 16 (7 sizes)
                    # Let's verify this mapping.
                    values = []
                    # The number of sizes we found:
                    num_sizes = len(self.sizes)
                    # We expect values at indices 4, 6, ... 4 + 2*(num_sizes-1)
                    for i in range(num_sizes):
                        idx = 4 + 2 * i
                        if idx < len(self.current_row):
                            values.append(self.clean_value(metric_name, self.current_row[idx]))
                        else:
                            values.append("")

                    if metric_name:
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
        if not name:
            return ""
        # Scott often has "metric name / translated name"
        if " / " in name:
            name = name.split(" / ")[0]
        name = name.lower()
        name = re.sub(r"[^a-z0-9]", "_", name)
        name = re.sub(r"_+", "_", name)
        return name.strip("_")

    def clean_value(self, metric_name, value):
        # Remove "mm" suffix
        value = value.replace("mm", "")
        # Remove "°" suffix
        value = value.replace("°", "")
        # Replace comma with dot
        value = value.replace(",", ".")
        # Remove any internal dots in what should be a single number (e.g. 1.006.4 -> 1006.4)
        if value.count(".") > 1:
            parts = value.split(".")
            value = "".join(parts[:-1]) + "." + parts[-1]
        if metric_name == "bb_offset" and value.startswith("-"):
            value = value[1:]

        return value.strip()


def parse_scott_geometry(html_path: str | Path, csv_path: str | Path):
    html_path = Path(html_path)
    csv_path = Path(csv_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    url_parser = ScottGeometryURLParser()
    url_parser.feed(html_content)

    if not url_parser.geometry_url:
        print(f"No geometry URL found in {html_path}")
        return

    # Fetch external geometry table
    ssl_context = ssl._create_unverified_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    }
    request = Request(url_parser.geometry_url, headers=headers)
    with urlopen(request, context=ssl_context) as response:
        table_html = response.read().decode("utf-8")

    table_parser = ScottGeometryTableParser()
    table_parser.feed(table_html)

    if not table_parser.sizes or not table_parser.metrics:
        print("No geometry data parsed from the table.")
        return

    metrics_list = list(table_parser.metrics.keys())
    header = ["size"] + metrics_list

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(header)

        for i, size in enumerate(table_parser.sizes):
            row = [size]
            for metric in metrics_list:
                values = table_parser.metrics[metric]
                if i < len(values):
                    row.append(values[i])
                else:
                    row.append("")
            writer.writerow(row)
