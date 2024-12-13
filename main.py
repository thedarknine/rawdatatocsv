"""
Main file to manage scripts
"""

import os
import sys
import pathlib
import json
import arrow
import toml
from dotenv import load_dotenv
from sources.models.process import Config
from sources.scripts import format_json, json_to_csv
from sources.utilities import display
from sources.utilities import files
from sources.utilities import logs

# Load env variables
try:
    load_dotenv(os.getenv("PROJECT_NAME"))
except FileNotFoundError:
    sys.exit(display.alert(f"Configuration could not be loaded {repr(Exception)}"))

display.clear_screen()

# Initialize logs
logger = logs.init_logger()

# Initialize script info
start_date = arrow.now(os.getenv("TIMEZONE", "Europe/Paris"))
display.start_info(start_date, "Formatting script")

if __name__ == "__main__":
    try:
        config = toml.load("process.toml")
        Config.model_validate(config)
    except toml.TomlDecodeError as e:
        print(f"TOML file is invalid: {e}")

    raw_path = pathlib.Path(os.getenv("DATA_RAW_DIR", "data"))
    proc_path = pathlib.Path(os.getenv("DATA_PROCESS_DIR", "process"))
    if not os.path.exists(proc_path):
        os.makedirs(proc_path)

    # Get process config
    for process in config["format_json"]["files"]:
        tmp_file = os.path.join(proc_path, process["output"])

        match process["method"]:
            case "split_by_line":
                content = files.get_content(process["filename"], raw_path)
                if content is not None and content != "":
                    display.info(
                        f"Processing {process['filename']} with {process['method']}"
                    )
                    formatted_content = format_json.split_by_line(content, process)
                    files.write(tmp_file, json.dumps(formatted_content, indent=4))
                else:
                    display.alert(
                        f"Cannot process {process['filename']} with {process['method']}"
                    )

            case "group_by_first":
                content = files.get_content(process["filename"], raw_path)
                if content is not None and content != "":
                    display.info(
                        f"Processing {process['filename']} with {process['method']}"
                    )
                    formatted_content = format_json.group_by_first(content)
                    files.write(tmp_file, json.dumps(formatted_content, indent=4))
                else:
                    display.alert(
                        f"Cannot process {process['filename']} with {process['method']}"
                    )

            case "split_by_object":
                display.info(
                    f"Processing {process['filename']} with {process['method']}"
                )
                content = files.get_content(process["filename"], raw_path)
                if content is not None and content != "":
                    display.info(
                        f"Processing {process['filename']} with {process['method']}"
                    )
                    formatted_content = format_json.split_by_object(content)
                    files.write(tmp_file, formatted_content)
                else:
                    display.alert(
                        f"Cannot process {process['filename']} with {process['method']}"
                    )

            case _:
                display.alert(f"Method {process['method']} is not valid")
                sys.exit(display.alert(f"Method {process['method']} is not valid"))

    if "json_to_csv" in config:
        data_csv = json_to_csv.compute_data(config["json_to_csv"])
        if data_csv is None:
            display.alert("Files missing, no data to compute")
        else:
            display.info(f"Processing {config['json_to_csv']['output']} with csv")
            csv_path = os.path.join(proc_path, config["json_to_csv"]["output"])
            files.write_csv(csv_path, data_csv)

    # Remove temporatory files
    tmp_path = pathlib.Path(os.getenv("DATA_TMP_DIR", ".tmp"))
    for file in tmp_path.iterdir() if tmp_path.exists() else []:
        file.unlink()

    # End script
    display.end_info(start_date)
    sys.exit()
