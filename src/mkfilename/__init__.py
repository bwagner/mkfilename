"""Turn an arbitrary string into a robust filename.

ASCII-only, lowercase, no spaces or shell-special chars.
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

# A trailing ".ext" is the only dot worth keeping. What follows the dot must be
# alphanumeric and run to the end, so "feat. Roberto" is not mistaken for one.
_EXTENSION_RE = re.compile(r"\.[A-Za-z0-9]+$")

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


def _underscore_dots(result):
    """Replace every dot with "_", except a trailing extension separator.

    Replacing rather than deleting keeps a word boundary: "a.b.c.d" becomes
    "a_b_c.d", not "abc.d". Where a space already followed the dot the extra
    "_" is merged away later by the _+ collapse.
    """
    match = _EXTENSION_RE.search(result)
    if match:
        return result[: match.start()].replace(".", "_") + match.group()
    return result.replace(".", "_")


def make_filename(title):
    """Turn title into a robust filename.

    ASCII-only, lowercase, no spaces or shell-special chars.
    """
    result = title.translate(TRANSLATIONS)
    result = unicodedata.normalize("NFKD", result).encode("ascii", "ignore").decode()
    # .lower() must follow this translate, not precede it: NFKD can yield a
    # char the table maps to uppercase (fullwidth "＄" -> "$" -> "S").
    result = result.translate(TRANSLATIONS).lower()
    result = _underscore_dots(result)
    result = re.sub(r"_+", "_", result).strip("_")
    if not result:
        return EMPTY_FALLBACK
    if result.startswith("."):
        result = "_" + result[1:]
    if len(result) > MAX_LENGTH:
        result = result[:MAX_LENGTH].rstrip("_") or EMPTY_FALLBACK
    return result
