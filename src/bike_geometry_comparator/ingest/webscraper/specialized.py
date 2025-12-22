import csv
import re
from html.parser import HTMLParser
from pathlib import Path


class SpecializedGeometryHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sizes = []
        self.metrics = {}  # metric_name -> [values]
        self.in_thead = False
        self.in_tbody = False
        self.in_th = False
        self.in_td = False
        self.row_data = []
        self.current_cell_data = []

    def handle_starttag(self, tag, attrs):
        if tag == "thead":
            self.in_thead = True
        elif tag == "tbody":
            self.in_tbody = True
        elif tag == "tr":
            self.row_data = []
        elif tag == "th":
            self.in_th = True
            self.current_cell_data = []
        elif tag == "td":
            self.in_td = True
            self.current_cell_data = []

    def clean_value(self, value):
        value = value.replace("mm", "")
        value = value.replace("°", "")
        value = value.replace("&deg", "")
        value = value.replace(",", ".")
        return value.strip()

    def clean_metric(self, name):
        name = name.lower()
        # Replace spaces with underscore
        name = name.replace(" ", "_")
        # Keep only lowercase letters and underscores (based on "should be lower-case letters")
        # But wait, if I keep only letters, then "top_tube_length,_horizontal" becomes "top_tube_length_horizontal"
        # Let's replace any non-alphanumeric with underscore and then collapse
        name = re.sub(r"[^a-z0-9]", "_", name)
        name = re.sub(r"_+", "_", name)
        return name.strip("_")

    def handle_endtag(self, tag):
        if tag == "thead":
            self.in_thead = False
        elif tag == "tbody":
            self.in_tbody = False
        elif tag == "tr":
            if self.in_thead:
                self.sizes = [d for d in self.row_data if d]
            elif self.in_tbody:
                if self.row_data:
                    metric_name = self.clean_metric(self.row_data[0])
                    values = [self.clean_value(v) for v in self.row_data[1:]]
                    self.metrics[metric_name] = values
        elif tag == "th":
            self.in_th = False
            self.row_data.append(" ".join(self.current_cell_data).strip())
        elif tag == "td":
            self.in_td = False
            self.row_data.append(" ".join(self.current_cell_data).strip())

    def handle_data(self, data):
        if self.in_th or self.in_td:
            self.current_cell_data.append(data.strip())


def parse_specialized_geometry(html_path: str | Path, csv_path: str | Path):
    html_path = Path(html_path)
    csv_path = Path(csv_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = SpecializedGeometryHTMLParser()
    parser.feed(html_content)

    if not parser.sizes or not parser.metrics:
        return

    # Pivot the data: sizes become rows, metrics become columns
    # Resulting CSV should have columns: size, metric1, metric2, ...

    metrics_list = list(parser.metrics.keys())
    header = ["size"] + metrics_list

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(header)

        for i, size in enumerate(parser.sizes):
            row = [size]
            for metric in metrics_list:
                values = parser.metrics[metric]
                if i < len(values):
                    row.append(values[i])
                else:
                    row.append("")
            writer.writerow(row)
