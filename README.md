# mkfilename

Turn an arbitrary string into a robust filename: ASCII-only, no spaces or shell-special chars.

```python
from mkfilename import make_filename

make_filename("Über Straße & Mäuse")   # 'Ueber_Strasse_and_Maeuse'
make_filename(".bashrc")                # '_bashrc'
make_filename("!!!")                    # 'untitled'
```

## Behavior

- German umlauts and `ß`: `ä→ae`, `ö→oe`, `ü→ue`, `Ä→Ae`, `Ö→Oe`, `Ü→Ue`, `ß→ss`
- Other accented Latin characters are stripped via NFKD + ASCII (`é→e`, `ñ→n`, ...)
- Whitespace, hyphens, en/em-dashes → `_`
- `&` → `and`, `$` → `S`
- Punctuation (`!?'"():;,*/|<>\#+`) is dropped
- Leading/trailing `_` are stripped
- Output is capped at 255 characters
- A leading `.` is replaced with `_` so the result isn't a hidden file
- Empty results fall back to `"untitled"`

## Install

```bash
pip install git+https://github.com/bwagner/mkfilename
# or with uv:
uv add git+https://github.com/bwagner/mkfilename
```

In a uv inline-script header:

```python
# /// script
# dependencies = ["mkfilename @ git+https://github.com/bwagner/mkfilename"]
# ///
```

## CLI

The package installs an `mkfilename` command (requires the `cli` extra for clipboard support):

```bash
pip install "mkfilename[cli] @ git+https://github.com/bwagner/mkfilename"
mkfilename "Über Straße"          # prints: Ueber_Strasse
mkfilename                         # reads from clipboard, writes back to clipboard
```

## Version

    mkfilename --version

Prints the bare version (e.g., `0.1.0`) when the project is not inside a git
repo, or an enriched `0.1.0 (git:<sha>[-dirty], <timestamp>)` when it is.

## Development

```bash
git clone https://github.com/bwagner/mkfilename
cd mkfilename
uv sync --all-extras
uv run pre-commit install
uv run pytest
```

### Lint and format

    uv run ruff check
    uv run ruff format

Pre-commit hooks run automatically on `git commit`.

### Editable global CLI

To install the `mkfilename` command globally, pointing at a local checkout so edits take effect immediately:

```bash
git clone https://github.com/bwagner/mkfilename
uv tool install --editable ./mkfilename --with pyperclip
```

`mkfilename` then resolves to `~/.local/bin/mkfilename` and runs against the source in your clone — no reinstall needed after edits.

## Update from pyskel

This project was scaffolded from [pyskel](https://github.com/bwagner/pyskel). Pull template improvements with:

    copier update

## License

MIT
