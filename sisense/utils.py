import json
import os


def is_windows() -> bool:
    """Check if OS is Windows. Otherwise, assume it is linux.

    :return: (bool) True, if OS is Windows. False, otherwise.
    """
    return os.name == 'nt'


def is_json(value: str) -> bool:
    """Check if string is a JSON parsable.

    :param value: (str) Value to check.
    :return: (bool) True, if value is a valid JSON string. False, otherwise.
    """
    try:
        _ = json.loads(value)
    except ValueError:
        return False

    return True
