import re
import unicodedata

__all__ = ["make_filename", "MAX_LENGTH", "EMPTY_FALLBACK", "TRANSLATIONS"]

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
    """Turn title into a robust filename: ASCII-only, no spaces or shell-special chars."""
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
