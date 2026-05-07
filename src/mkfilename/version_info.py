"""Return a version string enriched with git commit info."""

import os
import subprocess

_SRC_DIR = os.path.dirname(os.path.abspath(__file__))


def get_version_info(version: str) -> str:
    """Return version enriched with git commit, dirty flag, and timestamp.

    Queries the git repo that contains this source file. When the file is
    not inside a git repo (e.g. installed into site-packages outside a
    project tree), returns the plain version string.
    """
    try:
        rev = subprocess.check_output(
            ["git", "-C", _SRC_DIR, "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        dirty = subprocess.check_output(
            ["git", "-C", _SRC_DIR, "status", "--porcelain"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        ts = subprocess.check_output(
            ["git", "-C", _SRC_DIR, "log", "-1", "--format=%ai"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        suffix = "-dirty" if dirty else ""
        return f"{version} (git:{rev}{suffix}, {ts})"
    except Exception:
        return version
