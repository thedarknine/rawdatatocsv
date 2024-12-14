"""
Json to csv converter
"""

import json
import os
from sources.utilities import files


def compute_data(config: dict) -> list:
    """
    Compute files to convert json to csv

    Args:
        config (dict): Process config

    Returns:
        list: Content to write
    """
    listing = files.get_content(config["main_file"], os.getenv("DATA_PROCESS_DIR"))
    if listing is None:
        return None

    has_label = config["display_label"] if "display_label" in config else False
    headers = [item for item in json.loads(listing) if listing]
    if has_label:
        headers.insert(0, "LABEL")
    headers.insert(0, " ")
    csv_content = []
    csv_content.append(headers)

    has_count = config["display_count"] if "display_count" in config else False
    if has_count:
        count = {}
        for item in headers:
            if item not in (" ", "LABEL"):
                count[headers.index(item)] = 0

    for file in config["secondary_files"]:
        metas = {
            "has_label": has_label,
            "has_count": has_count,
            "count": count,
        }
        csv_content, count = extract_content(file, headers, csv_content, metas)

    # Add counters
    if has_count:
        row = []
        for item in headers:
            if item == " ":
                row.append("TOTAL")
            elif item == "LABEL":
                row.append(" ")
            else:
                row.append(str(count[headers.index(item)]))
        csv_content.append(row)

    return csv_content


def extract_content(
    file: str, headers: list, csv_content: list, metas: list = None
) -> list:
    """
    Extract  content

    Args:
        file (str): File name
        headers (list): Headers
        csv_content (list): Content to write
        has_label (bool): Has label
        has_count (bool): Has count
        count (list): Count

    Returns:
        list: Content to write and counter
    """
    count = metas["count"] if metas is not None else {}

    content = files.get_content(file, os.getenv("DATA_PROCESS_DIR"))
    if content is None:
        return None
    json_content = json.loads(content)
    label = str.replace(file, ".json", "") if metas["has_label"] else ""

    for info, list_items in json_content.items():
        tmp_list = []
        # pprint.pp("------------>" + info)
        # pprint.pp(list_items)

        for item in headers:
            if item not in (" ", "LABEL"):
                tmp_list.append(
                    str(list_items[item]) if item != "" and item in list_items else "-"
                )
                if metas["has_count"] and count is not None:
                    count[headers.index(item)] += (
                        1 if item != "" and item in list_items else 0
                    )

        row = [info, str.upper(label)] if metas["has_label"] else [info]
        for tmp_item in tmp_list:
            if tmp_item != "":
                row.append(tmp_item)
        csv_content.append(row)

    return csv_content, count
