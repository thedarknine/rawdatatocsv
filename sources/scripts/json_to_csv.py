"""
Json to csv converter
"""

import json
import os
from sources.utilities import files


def compute_data(config):
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
    headers = [item for item in json.loads(listing) if listing]
    headers.insert(0, "LABEL")
    headers.insert(0, " ")
    csv_content = []
    csv_content.append(headers)

    for file in config["secondary_files"]:
        content = files.get_content(file, os.getenv("DATA_PROCESS_DIR"))
        if content is None:
            return None
        json_content = json.loads(content)
        label = str.replace(file, ".json", "")

        for info, list_items in json_content.items():
            tmp_list = []
            # pprint.pp("------------>" + info)
            # pprint.pp(list_items)

            for item in headers:
                if item not in (" ", "LABEL"):
                    tmp_list.append(
                        item + str(list_items[item])
                        if item != "" and item in list_items
                        else "-"
                    )

            row = [info, str.upper(label)]
            for tmp_item in tmp_list:
                if tmp_item != "":
                    row.append(tmp_item)
            csv_content.append(row)

    return csv_content
