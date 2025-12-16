from __future__ import annotations

import csv
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional


class _CanyonGeometryHTMLParser(HTMLParser):
    """HTML parser tailored to Canyon product geometry table.

    Collects size headings and per‑metric rows from the table with class
    `geometryTable__table` present in saved product page HTML.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        # State flags
        self._in_table = False
        self._table_depth = 0
        self._in_thead = False
        self._in_tbody = False

        # Sizes (header) collected from THEAD buttons' data-size
        self.sizes: List[str] = []

        # Row collection: (origin, metric, values)
        # origin: "frame" for the first geometry table, "components" for the second,
        # fallback to "table{n}" for subsequent tables if present.
        self.rows: List[tuple[str, str, List[str]]] = []
        self._in_tr = False
        self._current_metric: Optional[str] = None
        self._current_values: List[str] = []

        # Flags to capture the first span text inside title cell
        self._in_title_inner = False
        self._need_metric_span = False
        self._in_metric_span = False

        # Capture when in a value span
        self._in_value_span = False

        # Track which geometry table we are in (frame/components by order)
        self._table_index = 0
        self._current_origin: Optional[str] = None

    @staticmethod
    def _class_has(class_attr: Optional[str], needle: str) -> bool:
        # Avoid calling split on None to satisfy type-checker
        if class_attr is None:
            return False
        return needle in class_attr.split()

    def handle_starttag(self, tag: str, attrs):
        attr = dict(attrs)
        if tag == "table":
            if self._class_has(attr.get("class"), "geometryTable__table"):
                self._in_table = True
                self._table_depth = 1
                # Determine origin by encountered order
                self._table_index += 1
                if self._table_index == 1:
                    self._current_origin = "frame"
                elif self._table_index == 2:
                    self._current_origin = "components"
                else:
                    self._current_origin = f"table{self._table_index}"
            elif self._in_table:
                # Nested table under the main one
                self._table_depth += 1
        elif self._in_table:
            if tag == "thead":
                self._in_thead = True
            elif tag == "tbody":
                self._in_tbody = True
            elif self._in_thead and tag == "button":
                # Size headings live in buttons with data-size
                size_val = attr.get("data-size")
                if isinstance(size_val, str):
                    self.sizes.append(size_val)
            elif self._in_tbody:
                if tag == "tr" and self._class_has(
                    attr.get("class"), "geometryTable__dataRow"
                ):
                    self._in_tr = True
                    self._current_metric = None
                    self._current_values = []
                elif (
                    self._in_tr
                    and tag == "div"
                    and self._class_has(attr.get("class"), "geometryTable__titleInner")
                ):
                    # Next span encountered contains the metric label
                    self._in_title_inner = True
                    self._need_metric_span = True
                elif (
                    self._in_tr
                    and tag == "span"
                    and self._in_title_inner
                    and self._need_metric_span
                ):
                    # First span inside title inner is the metric label
                    # Avoid spans like attribute letters if they come later
                    self._in_metric_span = True
                    self._need_metric_span = False
                elif (
                    self._in_tr
                    and tag == "span"
                    and self._class_has(attr.get("class"), "geometryTable__sizeData")
                ):
                    self._in_value_span = True

    def handle_endtag(self, tag: str):
        if tag == "table" and self._in_table:
            self._table_depth -= 1
            if self._table_depth <= 0:
                self._in_table = False
                self._current_origin = None
        elif not self._in_table:
            return

        if tag == "thead":
            self._in_thead = False
        elif tag == "tbody":
            self._in_tbody = False
        elif self._in_tbody:
            if tag == "tr" and self._in_tr:
                # finalize row if any metric captured
                if self._current_metric is not None:
                    origin: str = self._current_origin or "table"
                    self.rows.append(
                        (origin, self._current_metric.strip(), self._current_values)
                    )
                self._in_tr = False
                self._current_metric = None
                self._current_values = []
            elif tag == "div" and self._in_title_inner:
                self._in_title_inner = False
                self._need_metric_span = False
                self._in_metric_span = False
            elif tag == "span" and self._in_metric_span:
                self._in_metric_span = False
            elif tag == "span" and self._in_value_span:
                self._in_value_span = False

    def handle_data(self, data: str):
        if not self._in_table:
            return
        if self._in_tbody and self._in_tr:
            if self._in_metric_span:
                # Capture the metric label once
                if self._current_metric is None:
                    self._current_metric = data.strip()
            elif self._in_value_span:
                self._current_values.append(data.strip())


def write_canyon_geometry_csv(html_path: str | Path, csv_path: str | Path) -> None:
    """Parse Canyon geometry tables (bike + components) from an HTML file and
    write a merged CSV grouped by size.

    The CSV will have the following structure:
      metric,<SIZE1>,<SIZE2>,...
      <Metric name>,<value for SIZE1>,<value for SIZE2>,...

    Notes:
      - The page can contain two geometry tables (frame and components). This
        function aggregates rows from both tables into a single CSV.
      - Size headers are collected from table headings and de-duplicated while
        preserving their original order (e.g., 3XS, 2XS, XS, S, M, L, XL, 2XL).

    Args:
        html_path: Path to the saved Canyon product HTML (e.g., build/endurace.html).
        csv_path: Destination CSV path to write.
    """

    html_path = Path(html_path)
    csv_path = Path(csv_path)

    text = html_path.read_text(encoding="utf-8", errors="replace")
    parser = _CanyonGeometryHTMLParser()
    parser.feed(text)

    sizes = parser.sizes
    rows = parser.rows

    # De-duplicate sizes while preserving the first-seen order. This also
    # handles the case when sizes are collected from multiple tables.
    if sizes:
        seen: set[str] = set()
        dedup_sizes: list[str] = []
        for s in sizes:
            if s not in seen:
                seen.add(s)
                dedup_sizes.append(s)
        sizes = dedup_sizes

    # Fallback: sometimes size headings are hidden in thead; if no sizes found,
    # infer the count from the first data row
    if not sizes and rows:
        sizes = [f"S{i + 1}" for i in range(len(rows[0][1]))]

    # Helper to normalize metric names: lower-case and spaces -> underscores
    def _norm(name: str) -> str:
        return "_".join(name.strip().lower().split())

    # Aggregate by normalized metric name and origin
    # base -> {origin: values}

    base_order: list[str] = []
    base_to_origin_values: dict[str, dict[str, List[str]]] = {}

    origin: str | None
    for origin, metric, values in rows:
        base = _norm(metric)
        if base not in base_to_origin_values:
            base_to_origin_values[base] = {}
            base_order.append(base)
        # In case of duplicates inside the same origin, prefer first occurrence
        base_to_origin_values[base].setdefault(origin, list(values))

    # Build columns list. If a base appears in both frame and components,
    # create two columns with prefixes; otherwise keep the base as-is.
    columns: list[str] = []
    column_specs: list[tuple[str, str | None]] = []  # (column_name, origin_if_prefixed)
    for base in base_order:
        origins = base_to_origin_values[base]
        has_frame = "frame" in origins
        has_components = "components" in origins
        if has_frame and has_components:
            columns.append(f"frame_{base}")
            column_specs.append((f"frame_{base}", "frame"))
            columns.append(f"components_{base}")
            column_specs.append((f"components_{base}", "components"))
        else:
            columns.append(base)
            # store None to indicate single-origin (whichever exists)
            column_specs.append((base, None))

    # Write pivoted CSV: rows are sizes
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["size", *columns])

        size_count = len(sizes)

        # Pre-pad/truncate all values to size_count
        def _norm_vals(vals: List[str]) -> List[str]:
            v = list(vals)
            if len(v) < size_count:
                v += [""] * (size_count - len(v))
            elif len(v) > size_count:
                v = v[:size_count]
            return v

        # Build a per-base, per-origin normalized values lookup
        base_origin_to_vals: dict[tuple[str, str], List[str]] = {}
        base_to_single_vals: dict[str, List[str]] = {}
        for base, origin_map in base_to_origin_values.items():
            if "frame" in origin_map:
                base_origin_to_vals[(base, "frame")] = _norm_vals(origin_map["frame"])
            if "components" in origin_map:
                base_origin_to_vals[(base, "components")] = _norm_vals(
                    origin_map["components"]
                )
            # choose whichever origin exists for single-origin bases
            if len(origin_map) == 1:
                only_vals = next(iter(origin_map.values()))
                base_to_single_vals[base] = _norm_vals(only_vals)

        # Emit one row per size index
        for idx, size in enumerate(sizes):
            row: list[str] = [size]
            base_or_pref: str
            for base_or_pref, origin in column_specs:
                if origin is None:
                    # single-origin base: use base name stored before stripping prefix
                    base_name = base_or_pref
                    vals = base_to_single_vals.get(base_name, [""] * size_count)
                    row.append(vals[idx] if idx < len(vals) else "")
                else:
                    # prefixed column: extract base after known prefix
                    if origin == "frame" and base_or_pref.startswith("frame_"):
                        base = base_or_pref[len("frame_") :]
                    elif origin == "components" and base_or_pref.startswith(
                        "components_"
                    ):
                        base = base_or_pref[len("components_") :]
                    else:
                        base = base_or_pref
                    vals = base_origin_to_vals.get((base, origin), [""] * size_count)
                    row.append(vals[idx] if idx < len(vals) else "")
            writer.writerow(row)


def crawl(html: Path, out_csv: Path) -> None:
    write_canyon_geometry_csv(html, out_csv)
