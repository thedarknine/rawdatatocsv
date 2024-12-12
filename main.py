"""
Main file to manage scripts
"""

import os
import sys
import pathlib
import json
import re
import arrow
import toml
from dotenv import load_dotenv
from sources.models.process import Config
from sources.scripts import format_json
from sources.utilities import display
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

    # Get process config
    # pprint.pp(config["format_json"])
    for process in config["format_json"]["files"]:
        match process["method"]:
            case "split_by_line_to_dict":
                display.info(
                    f"Processing {process['filename']} with {process['method']}"
                )
                formatted_content = {}
                with open(
                    os.path.join(raw_path, process["filename"]),
                    "rt",
                    encoding=os.getenv("ENCODING"),
                ) as inputfile:
                    content = inputfile.read()
                    inputfile.close()
                    if "header_line" in process and process["header_line"]:
                        regex = process["header_regex"]
                        for s in re.split(regex, content):
                            if s.strip() != "":
                                info = s.split("-", 1)
                                formatted_content[info[0]] = info[1]

                tmp_file = os.path.join(proc_path, process["output"])
                if not os.path.exists(proc_path):
                    os.makedirs(proc_path)
                with open(tmp_file, "w", encoding=os.getenv("ENCODING")) as outputfile:
                    outputfile.write(json.dumps(formatted_content, indent=4))
                    outputfile.close()

            case "group_by_first":
                display.info(
                    f"Processing {process['filename']} with {process['method']}"
                )
                formatted_content = {}
                with open(
                    os.path.join(raw_path, process["filename"]),
                    "rt",
                    encoding=os.getenv("ENCODING"),
                ) as inputfile:
                    content = inputfile.read()
                    inputfile.close()
                    formatted_content = format_json.group_by_first(content)

                tmp_file = os.path.join(proc_path, process["output"])
                if not os.path.exists(proc_path):
                    os.makedirs(proc_path)
                with open(tmp_file, "w", encoding=os.getenv("ENCODING")) as outputfile:
                    outputfile.write(json.dumps(formatted_content, indent=4))
                    outputfile.close()

    # Remove temporatory files
    tmp_path = pathlib.Path(os.getenv("DATA_TMP_DIR", ".tmp"))
    for file in tmp_path.iterdir():
        file.unlink()

    # End script
    display.end_info(start_date)
    sys.exit()
