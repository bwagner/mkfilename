"""Command-line entry point for mkfilename."""

from __future__ import annotations

import argparse

from . import __version__, get_version_info, make_filename


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mkfilename",
        description=(
            "Turn an arbitrary string into a robust filename: "
            "ASCII-only, lowercase, no spaces or shell-special chars."
        ),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=get_version_info(__version__),
    )
    parser.add_argument(
        "title",
        nargs="?",
        help="String to convert. If omitted, read from clipboard and write back.",
    )
    args = parser.parse_args(argv)

    if args.title is not None:
        print(make_filename(args.title))
        return 0

    import pyperclip

    clipboard = pyperclip.paste().strip()
    if not clipboard:
        parser.print_help()
        return 1
    print(f"clipboard had: {clipboard}")
    content = make_filename(clipboard)
    print(f"clipboard contains: {content}")
    pyperclip.copy(content)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
