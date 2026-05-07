"""Turn an arbitrary string into a robust filename.

ASCII-only, no spaces or shell-special chars.
"""

import re
import unicodedata
from importlib.metadata import PackageNotFoundError, version

from .version_info import get_version_info

try:
    __version__ = version("mkfilename")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+uninstalled"

__all__ = [
    "EMPTY_FALLBACK",
    "MAX_LENGTH",
    "TRANSLATIONS",
    "__version__",
    "get_version_info",
    "make_filename",
]

MAX_LENGTH = 255
EMPTY_FALLBACK = "untitled"

TRANSLATIONS = {
    ord(k): v
    for k, v in {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
        " ": "_",
        "\n": "_",
        "\t": "_",
        "\r": "_",
        "-": "_",
        "–": "_",
        "—": "_",
        "&": "and",
        "$": "S",
        "+": "",
        "(": "",
        ")": "",
        "?": "",
        "!": "",
        "'": "",
        '"': "",
        ":": "",
        ";": "",
        ",": "",
        "*": "",
        "/": "",
        "|": "",
        "<": "",
        ">": "",
        "\\": "",
        "#": "",
    }.items()
}


def make_filename(title):
    """Turn title into a robust filename.

    ASCII-only, no spaces or shell-special chars.
    """
    result = title.translate(TRANSLATIONS)
    result = unicodedata.normalize("NFKD", result).encode("ascii", "ignore").decode()
    result = result.translate(TRANSLATIONS)
    result = re.sub(r"_+", "_", result).strip("_")
    if not result:
        return EMPTY_FALLBACK
    if result.startswith("."):
        result = "_" + result[1:]
    if len(result) > MAX_LENGTH:
        result = result[:MAX_LENGTH].rstrip("_") or EMPTY_FALLBACK
    return result
