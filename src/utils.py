import re


def to_snake_case(key: str) -> str:
    """
    Convert a camelCase or PascalCase string to snake_case.

    Parameters
    ----------
    key : str
        The input string in camelCase or PascalCase.

    Returns
    -------
    str
        The converted string in snake_case.
    """
    converted = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
    return converted


def to_camel_case(key: str) -> str:
    """
    Convert a snake_case string to camelCase.

    Parameters
    ----------
    key : str
        The input string in snake_case.

    Returns
    -------
    str
        The converted string in camelCase.
    """
    converted = re.sub(r"_([a-z])", lambda match: match.group(1).upper(), key)
    return converted
