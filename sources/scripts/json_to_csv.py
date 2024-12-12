import pprint
import json
import csv
import os
from sources.utilities import files

def compute_data(config):
    # pprint.pprint(config)
    listing = files.get_content(config["main_file"], os.getenv("DATA_PROCESS_DIR"))
    headers = [item for item in json.loads(listing) if listing]
    headers.insert(0, "LABEL")
    headers.insert(0," ")
    csv_content = []
    csv_content.append(headers)

    for file in config["secondary_files"]:
        content = files.get_content(file, os.getenv("DATA_PROCESS_DIR"))
        json_content = json.loads(content)
        label = str.replace(file, ".json", "")
        # print(json_content)

        for info,list_items in json_content.items():
            tmp_list = []
            # pprint.pp("------------>" + info)
            # pprint.pp(list_items)

            for item in headers:
                tmp_list.append(str(list_items[item]) if item != "" and item in list_items else "-")

            row = [info, str.upper(label)]
            for tmp_item in tmp_list:
                if tmp_item != "":
                    row.append(tmp_item)
            # pprint.pp(row)
            csv_content.append(row)
            if info =="drive.trilport.fr":
                pprint.pp(row)
            
    #pprint.pprint(csv_content)
    return csv_content
