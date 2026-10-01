#!/usr/bin/env python3
"""
run_all.py — execute every Python code block inside every lesson.

Usage:
    python run_all.py                    # check every lesson
    python run_all.py part03_linear_algebra
    python run_all.py 36                 # only lessons in part 03
    python run_all.py --show 36          # also print each block's output

Why this exists
---------------
A lesson that claims a computation gives 0.8660 is worthless if the code no
longer produces 0.8660. This script extracts the fenced ```python blocks from
every markdown file and runs them, so the examples cannot silently rot.

Blocks are run in a fresh namespace, in file order, and top-level code only.
A block that imports a third-party package fails loudly rather than being
skipped, because a broken example is a real problem.
"""

from __future__ import annotations

import io
import re
import sys
import time
import traceback
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FENCE_RE = re.compile(
    r"^```python\s*\n(.*?)^```",
    re.MULTILINE | re.DOTALL | re.VERBOSE,
)

# Blocks that are deliberately non-executable: illustrations, pseudocode, and
# fragments the lesson explicitly marks as not runnable.
SKIP_MARKERS = ("not runnable", "pseudocode", "output:", "# (skipped)")


def blocks_in(path: Path) -> list[str]:
    """Return every ```python block in the file that should be executed."""
    text = path.read_text(encoding="utf-8")
    out = []
    for match in FENCE_RE.finditer(text):
        code = match.group(1)
        # Look at the line just above the fence for a skip marker.
        start = match.start()
        preceding = text[max(0, start - 200) : start].lower()
        if any(marker in preceding[-120:] for marker in SKIP_MARKERS):
            continue
        if code.strip().startswith((">>>", "$")):
            continue  # REPL transcript, not a script
        out.append(code)
    return out


def run_block(code: str) -> tuple[bool, str, str]:
    """Run one block. Return (ok, stdout, error_text)."""
    buffer = io.StringIO()
    namespace = {"__name__": "__lesson__"}
    try:
        with redirect_stdout(buffer):
            exec(compile(code, "<lesson>", "exec"), namespace)
    except Exception:
        return False, buffer.getvalue(), traceback.format_exc(limit=3)
    return True, buffer.getvalue(), ""


def main() -> int:
    args = sys.argv[1:]
    show = "--show" in args
    if show:
        args.remove("--show")
    wanted = args[0] if args else None

    files = sorted(
        p
        for p in ROOT.rglob("*.md")
        if p.parent.name.startswith("part")
    )

    total_blocks = 0
    failed: list[tuple[str, int, str]] = []
    started = time.time()

    for path in files:
        if wanted:
            rel = path.relative_to(ROOT).as_posix()
            key = wanted.zfill(2)
            if key not in rel and wanted not in rel:
                continue

        blocks = blocks_in(path)
        if not blocks:
            continue
        rel = path.relative_to(ROOT).as_posix()

        for i, code in enumerate(blocks, start=1):
            total_blocks += 1
            ok, out, err = run_block(code)
            status = "ok  " if ok else "FAIL"
            print(f"  [{status}] {rel} block {i}")
            if show and out:
                for line in out.rstrip().splitlines():
                    print(f"         | {line}")
            if not ok:
                failed.append((rel, i, err))

    elapsed = time.time() - started
    print()
    print(f"  {total_blocks} code blocks from {len(files)} files in {elapsed:.1f}s")
    if failed:
        print(f"  {len(failed)} FAILURES")
        print()
        for rel, i, err in failed:
            print(f"  --- {rel} block {i} " + "-" * 40)
            print(err)
            print()
        return 1

    print("  all code blocks executed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())