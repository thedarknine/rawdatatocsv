"""
Tools to handle raw data
"""

OPEN_BRACKET = "{\n"
CLOSE_BRACKET = "\n}"
COMMA = ","


def split_by_line_to_dict(content: str) -> dict:
    """
    Split content by line and create a dictionary

    Args:
        content (str): Content to split

    Returns:
        dict: Dictionary
    """
    content = str.replace(content, '"', "")
    split_content = content.split("\n")
    split_dict = {}
    for line in split_content:
        split = line.split(":")
        if len(split) == 2:
            split_dict[split[0]] = split[1]
    return split_dict


def group_by_first(content: str):
    """
    Split content, group by first item of line and create a dictionary

    Args:
        content (str): Content to split

    Returns:
        dict: Dictionary
    """
    split_content = content.split("\n")
    split_dict = {}
    for line in split_content:
        info = line.split(";")
        if info[0] not in split_dict:
            split_dict[info[0]] = {}
        # pprint.pp(split)
        if len(info) == 2:
            version = info[1].rsplit("-", 1)
            split_dict[info[0]][version[0]] = version[1]
    return split_dict


def add_global_brackets(content):
    """
    Add global brackets to content

    Args:
        content (str): Content to add brackets

    Returns:
        str: Content with brackets
    """
    return OPEN_BRACKET + content + CLOSE_BRACKET


def add_comma_by_line(content):
    """
    Add comma by line to content

    Args:
        content (str): Content to add comma

    Returns:
        str: Content with comma
    """
    return str.replace(content, "\n", COMMA + "\n")
