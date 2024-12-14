"""
Process model to validate toml config file
"""
from pydantic import BaseModel


class JsonFile(BaseModel):
    """Json file model"""
    filename: str
    header_line: bool | None = None
    header_regex: str | None = None
    output: str
    method: str


class CSVFile(BaseModel):
    """Csv file model"""
    main_file: str
    secondary_files: list[str]
    output: str
    display_label: bool | None = None
    display_count: bool | None = None


class FormatJson(BaseModel):
    """Format json model"""
    name: str
    files: list[JsonFile]


class Config(BaseModel):
    """Config model"""
    format_json: FormatJson
    json_to_csv: CSVFile
