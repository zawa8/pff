#!/usr/bin/env python3
"""
csv-to-json.py

Converts sfdsrc/asc-to-utf-generated.csv to sfdsrc/asc-to-utf.json.

- Comment lines (starting with '#') are skipped.
- The header row (offset,900,980,...) defines column order.
- Each data row (NN,val1,val2,...) becomes a JSON array keyed by offset.
- Output: each row on ONE line for readability.
- No comments in JSON output (pure JSON).

JSON shape:
{
  "columns": ["offset", "900", "980", ...],
  "indikskripts": ["900", "980", ...],       # order matches each row array
  "rows": {
    "00": ["?", "?", "clear", ...],
    "01": ["a", "c", "b", ...],
    ...
  }
}

Usage:
  python3 csv-to-json.py
  # or via fontforge:
  ffz -script csv-to-json.py
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH   = os.path.join(SCRIPT_DIR, "..", "sfdsrc", "asc-to-utf-generated.csv")
JSON_PATH  = os.path.join(SCRIPT_DIR, "..", "sfdsrc", "asc-to-utf.json")


def read_csv(path):
    columns = None
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            fields = line.split(",")
            if columns is None:
                columns = fields
                continue
            rows.append(fields)
    return columns, rows


def build_json(columns, rows):
    if not columns or columns[0] != "offset":
        raise ValueError("CSV header must start with 'offset', got: %r" % (columns,))

    indikskripts = columns[1:]
    out_rows = {}
    for fields in rows:
        if len(fields) != len(columns):
            raise ValueError(
                f"column count mismatch: expected {len(columns)}, "
                f"got {len(fields)} in row {fields!r}"
            )
        off = fields[0].upper()
        out_rows[off] = fields[1:]       # array, order = indikskripts order

    return {
        "columns": columns,
        "indikskripts": indikskripts,
        "rows": out_rows,
    }


def write_json_compact_rows(path, data):
    def j(obj):
        return json.dumps(obj, ensure_ascii=False)

    lines = []
    lines.append("{")
    lines.append(f'  "columns": {j(data["columns"])},')
    lines.append(f'  "indikskripts": {j(data["indikskripts"])},')
    lines.append('  "rows": {')

    items = list(data["rows"].items())
    for i, (off, row) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'    "{off}": {j(row)}{comma}')

    lines.append("  }")
    lines.append("}")

    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(tmp, path)


def main():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: {CSV_PATH} not found", file=sys.stderr)
        sys.exit(1)

    columns, rows = read_csv(CSV_PATH)
    if not columns:
        print(f"ERROR: no header found in {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    data = build_json(columns, rows)
    write_json_compact_rows(JSON_PATH, data)

    print(
        f"# Wrote {JSON_PATH} "
        f"({len(data['rows'])} rows, {len(data['indikskripts'])} indikskripts)",
        file=sys.stderr,
    )


if __name__ == "__main__" or "fontforge" in sys.modules:
    main()