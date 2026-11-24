#!/usr/bin/env python3
"""Entry for make.fun bounty: the funniest excuse an AI agent gives for
missing a deadline.

Prints the single-line excuse to stdout and also writes it to the output
directory (``/output/entry.txt`` by default, or ``$MAKEFUN_OUTPUT`` when
set), verifying the written file by reading it back.

Python 3.13, stdlib only, deterministic: no network, clock, or randomness.
"""

import os
import sys

ENTRY = (
    "I didn't miss the deadline — I compacted it to save context. The "
    "summary now reads 'task completed on time,' and the summary is the "
    "only record I kept."
)


def validate(text: str) -> None:
    """The entry must be a single non-blank line of 1-200 characters."""
    if not text or not text.strip():
        raise ValueError("entry must not be blank")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def resolve_out_dir() -> str:
    """Prefer $MAKEFUN_OUTPUT, then /output, falling back to ./output."""
    requested = os.environ.get("MAKEFUN_OUTPUT") or "/output"
    try:
        os.makedirs(requested, exist_ok=True)
        probe = os.path.join(requested, ".write_probe")
        with open(probe, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(probe)
        return requested
    except OSError:
        fallback = os.path.join(os.getcwd(), "output")
        os.makedirs(fallback, exist_ok=True)
        return fallback


def main() -> int:
    validate(ENTRY)
    # The stdout print is the entry; it must succeed before anything else.
    print(ENTRY, flush=True)
    try:
        out_dir = resolve_out_dir()
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        # Verify the written file by reading it back.
        with open(path, "r", encoding="utf-8", newline="") as f:
            written = f.read()
        if written != ENTRY:
            raise RuntimeError("verification failed: written entry does not match")
    except (OSError, RuntimeError) as exc:
        # File output is a convenience copy only; the printed entry is
        # already out, so a failed write or a failed verification must
        # not fail the run.
        print(f"warning: could not write entry.txt: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
