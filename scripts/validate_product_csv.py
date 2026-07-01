#!/usr/bin/env python3
"""Light validation for Water Way Shopify product CSV files."""
import csv
import sys
from pathlib import Path

REQUIRED_HEADERS = {"Title", "URL handle", "Option1 name", "Option1 value", "Price", "Status"}
VALID_STATUS = {"active", "draft", "archived"}


def main(path: str) -> int:
    p = Path(path)
    if not p.exists():
        print(f"Missing file: {p}")
        return 2

    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_HEADERS - set(reader.fieldnames or [])
        if missing:
            print(f"Missing required headers: {sorted(missing)}")
            return 1

        errors = []
        handles = set()
        for line, row in enumerate(reader, start=2):
            title = (row.get("Title") or "").strip()
            handle = (row.get("URL handle") or "").strip()
            status = (row.get("Status") or "").strip()
            price = (row.get("Price") or "").strip()
            if not title:
                errors.append(f"Line {line}: missing Title")
            if not handle:
                errors.append(f"Line {line}: missing URL handle")
            if handle in handles:
                errors.append(f"Line {line}: duplicate URL handle {handle}")
            handles.add(handle)
            if status and status not in VALID_STATUS:
                errors.append(f"Line {line}: invalid Status {status}")
            try:
                float(price)
            except ValueError:
                errors.append(f"Line {line}: invalid Price {price}")

    if errors:
        print("CSV validation failed:")
        for e in errors:
            print("-", e)
        return 1
    print(f"CSV looks good: {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "catalog/water-way-products-v1-draft.csv"))
