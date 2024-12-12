"""
File utility tools
"""

import os


def get_content(filename: str, filepath: str) -> str:
    """
    Get content of file

    Args:
        filename (str): File name
        filepath (str): File path

    Returns:
        str: Content of file
    """
    with open(
        os.path.join(filepath, filename),
        "rt",
        encoding=os.getenv("ENCODING"),
    ) as inputfile:
        content = inputfile.read()
        inputfile.close()
        return content
    return ""


def write(filename: str, content: str) -> None:
    """
    Write content to file

    Args:
        filename (str): File name
        content (str): Content to write
    """
    with open(filename, "w", encoding=os.getenv("ENCODING")) as outputfile:
        outputfile.write(content)
        outputfile.close()
