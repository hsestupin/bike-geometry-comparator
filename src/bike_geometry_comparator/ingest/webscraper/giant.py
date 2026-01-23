import csv
import re
from html.parser import HTMLParser
from pathlib import Path


class GiantGeometryHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sizes = []
        self.metrics = {}  # metric_name -> [values]
        self.in_thead = False
        self.in_tbody = False
        self.in_th = False
        self.in_td = False
        self.in_name_cell = False
        self.in_value_mm = False
        self.in_degrees = False
        self.row_data = []
        self.current_metric_name = ""
        self.current_cell_values = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "")

        if tag == "thead":
            self.in_thead = True
        elif tag == "tbody":
            self.in_tbody = True
        elif tag == "tr":
            self.row_data = []
            self.current_metric_name = ""
        elif tag == "th":
            self.in_th = True
        elif tag == "td":
            self.in_td = True
            self.current_cell_values = []
            if "name" in classes:
                self.in_name_cell = True
        elif tag == "span":
            if "value-mm" in classes:
                self.in_value_mm = True
            elif "degrees" in classes:
                self.in_degrees = True

    def clean_value(self, value):
        # Remove mm suffix
        value = value.replace("mm", "")
        # Remove degree symbol and replace comma with dot
        value = value.replace("°", "")
        value = value.replace(",", ".")
        return value.strip()

    def clean_metric(self, name):
        # Remove the letter code prefix like "A ", "B ", etc.
        name = re.sub(r"^[A-Z]\s+", "", name)
        # Remove unit labels like (mm), (inch), (degrees)
        name = re.sub(r"\s*\([^)]*\)\s*", " ", name)
        # Convert to lowercase
        name = name.lower()
        # Replace spaces with underscore
        name = name.replace(" ", "_")
        # Replace any non-alphanumeric with underscore and collapse
        name = re.sub(r"[^a-z0-9]", "_", name)
        name = re.sub(r"_+", "_", name)
        # Handle special cases
        if name == "b_b_height":
            name = "bb_height"
        elif name == "b_b_drop":
            name = "bb_drop"
        return name.strip("_")

    def handle_endtag(self, tag):
        if tag == "thead":
            self.in_thead = False
        elif tag == "tbody":
            self.in_tbody = False
        elif tag == "tr":
            if self.in_thead:
                # Extract sizes from header row (skip first empty column)
                self.sizes = [s for s in self.row_data if s]
            elif self.in_tbody and self.current_metric_name:
                # Store metric values
                metric_name = self.clean_metric(self.current_metric_name)
                if metric_name:
                    self.metrics[metric_name] = self.row_data
        elif tag == "th":
            self.in_th = False
        elif tag == "td":
            if self.in_name_cell:
                self.in_name_cell = False
            else:
                # This is a value cell - add the collected value
                if self.current_cell_values:
                    self.row_data.append(self.clean_value(self.current_cell_values[0]))
                else:
                    self.row_data.append("")
            self.in_td = False
            self.current_cell_values = []
        elif tag == "span":
            self.in_value_mm = False
            self.in_degrees = False

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return

        if self.in_thead and self.in_th:
            # Collect size names from header
            if data and data != "\xa0":  # Skip non-breaking space
                self.row_data.append(data)
        elif self.in_tbody:
            if self.in_name_cell:
                # Collect metric name (skip the letter code span content)
                if not re.match(r"^[A-Z]$", data):
                    self.current_metric_name += " " + data
            elif self.in_value_mm or self.in_degrees:
                # Collect the mm value or degree value
                self.current_cell_values.append(data)


def parse_giant_geometry(html_path: str | Path, csv_path: str | Path):
    html_path = Path(html_path)
    csv_path = Path(csv_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = GiantGeometryHTMLParser()
    parser.feed(html_content)

    if not parser.sizes or not parser.metrics:
        return

    # Pivot the data: sizes become rows, metrics become columns
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
