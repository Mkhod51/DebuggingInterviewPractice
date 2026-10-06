"""CSV decoding and per-row validation."""
import csv
import io
import math
from .models import Record

REQUIRED = {"id", "text", "weight"}
OPTIONAL = {"label"}


def read_rows(text):
    reader = csv.DictReader(text.splitlines(keepends = True))
    headers = reader.fieldnames
    if headers is None or not REQUIRED.issubset(headers):
        raise ValueError("Missing required headers")
    if len(headers) != len(set(headers)):
        raise ValueError("Duplicate headers")
    if set(headers) - REQUIRED - OPTIONAL:
        raise ValueError("Unknown headers")
    return list(reader)


def parse_record(row):
    if None in row:
        raise ValueError("Too many fields")
    if any(row.get(name) is None for name in REQUIRED):
        raise ValueError("Missing required value")
    identifier = row["id"].strip()
    if not identifier:
        raise ValueError("Empty ID")
    text = row["text"]
    if not text:
        raise ValueError("Empty text")
    try:
        weight = float(row["weight"])
    except ValueError:
        raise ValueError("Invalid weight") from None
    if not math.isfinite(weight) or not 0 < weight <= 1:
        raise ValueError("Weight outside bounds")
    label = row.get("label")
    if label is None:
        label = "unlabeled"
    return Record(identifier, text, weight, label)
