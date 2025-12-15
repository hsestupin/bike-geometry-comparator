from __future__ import annotations

from typing import Iterable, Sequence


def format_table(
    rows: Iterable[Sequence[object]],
    headers: Sequence[str] | None = None,
    max_rows: int | None = None,
) -> str:
    """
    Build a simple ASCII table string from an iterable of row sequences (e.g., list of tuples)
    like those returned by `duckdb.execute(...).fetchall()`.

    - `headers`: optional column names (use `cursor.description` to obtain them)
    - `max_rows`: if provided, limits the number of displayed rows
    """

    # Materialize rows (we need to iterate them multiple times)
    materialized = list(rows)
    if max_rows is not None:
        materialized = materialized[:max_rows]

    if not materialized and not headers:
        return "<empty result>"

    # Infer column count
    col_count = 0
    if headers:
        col_count = len(headers)
    if materialized:
        col_count = max(col_count, len(materialized[0]))

    # Normalize headers length
    norm_headers = list(headers) if headers else []
    if len(norm_headers) < col_count:
        norm_headers += [f"col{i + 1}" for i in range(len(norm_headers), col_count)]

    # Compute column widths
    widths = [len(str(h)) for h in norm_headers]
    for row in materialized:
        for i in range(col_count):
            cell = row[i] if i < len(row) else ""
            widths[i] = max(widths[i], len(_format_cell(cell)))

    # Build helpers
    def sep(char: str = "-") -> str:
        parts = [char * (w + 2) for w in widths]
        return "+" + "+".join(parts) + "+"

    def fmt_row(values: Sequence[object]) -> str:
        cells = []
        for i in range(col_count):
            val = values[i] if i < len(values) else ""
            sval = _format_cell(val)
            cells.append(" " + sval.ljust(widths[i]) + " ")
        return "|" + "|".join(cells) + "|"

    lines: list[str] = []
    # Header
    lines.append(sep("-"))
    lines.append(fmt_row(norm_headers))
    lines.append(sep("-"))

    # Body
    for row in materialized:
        lines.append(fmt_row(row))

    lines.append(sep("-"))

    # Indicate truncation
    if max_rows is not None and len(rows) > max_rows:
        lines.append(f"… {len(rows) - max_rows} more rows not shown …")

    return "\n".join(lines)


def _format_cell(val: object) -> str:
    if val is None:
        return "NULL"
    return str(val)
