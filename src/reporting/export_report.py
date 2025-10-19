import os
import csv
import json
from typing import Any, Dict, List, Union

def export_report(data: Union[List[Dict[str, Any]], Dict[str, Any]],
                  output_path: str,
                  file_type: str = "csv") -> None:
    """
    Export data to CSV or JSON file for sharing and reporting.

    Parameters
    ----------
    data : list[dict] or dict
        Data to export
    output_path : str
        File path to save the report
    file_type : str
        "csv" or "json" (default: csv)

    Raises
    ------
    ValueError
        If inputs are invalid.
    """
    if not isinstance(data, (list, dict)) or not data:
        raise ValueError("Data must be a non-empty list or dict")
    if not isinstance(output_path, str) or not output_path.strip():
        raise ValueError("output_path must be a non-empty string")
    if file_type not in {"csv", "json"}:
        raise ValueError("file_type must be 'csv' or 'json'")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if file_type == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    elif file_type == "csv":
        if isinstance(data, dict):
            data = [data]
        keys = set().union(*(d.keys() for d in data))
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(keys))
            writer.writeheader()
            writer.writerows(data)
