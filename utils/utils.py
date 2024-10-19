import json
import os
from enum import Enum


class FormatType(Enum):
    TEXT = 'text'
    JSON = 'json'


def _load_file(path, file_name, formatType: FormatType = FormatType.JSON):
    file_path = os.path.join(os.path.dirname(__file__), path, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        if formatType == FormatType.JSON:
            return json.load(file)
        else:
            return file.read()


def fetch_function(file_name):
    return _load_file('../functions', file_name, FormatType.JSON)


def fetch_prompt(file_name):
    return _load_file('../prompt', file_name, FormatType.TEXT)
