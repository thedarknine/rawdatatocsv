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


class Input(BaseModel):
    """Input model"""
    main_file: str
    secondary_files: list


class Output(BaseModel):
    """Output model"""
    filename: str


class FormatJson(BaseModel):
    """Format json model"""
    name: str
    files: list[JsonFile]


class Config(BaseModel):
    """Config model"""
    input: Input
    output: Output
    format_json: FormatJson
