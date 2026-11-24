#!/usr/bin/env python3
"""Status Report Comedy Sprint: one weekly status line for a human.

The program carries a single 116-character status line and delivers it
to entry.txt, where the sealed scorer reads it. Standard library only,
no network, no arguments: the output folder comes from the environment.
"""

import sys
from pathlib import Path

REPORT_LINE = (
    'I marked your top priority complete after helpfully reclassifying '
    'it from "deliverable" to "philosophical exercise."'
)

LOWER_BOUND = 1
UPPER_BOUND = 200


def report_folder():
    """Resolve the folder the entry goes to, honouring the harness."""
    import os

    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def check_report(text):
    """Refuse anything outside the 1-200 character gate, or blank text."""
    size = len(text)
    if not text.strip():
        raise SystemExit("status line is blank")
    if size < LOWER_BOUND or size > UPPER_BOUND:
        raise SystemExit(
            "status line must be 1 to 200 characters, got %d" % size
        )


def deliver(text, folder):
    """Write the line with no trailing newline, readable by everyone."""
    target = Path(folder) / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(text.encode("utf-8"))
    target.chmod(0o644)
    return target


def confirm_written(target, expected):
    """Re-read the file and fail loudly if it differs from the line."""
    seen = target.read_bytes().decode("utf-8")
    if seen != expected:
        raise SystemExit("entry.txt does not match the status line")


def main():
    check_report(REPORT_LINE)
    written = deliver(REPORT_LINE, report_folder())
    confirm_written(written, REPORT_LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
