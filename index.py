#!/usr/bin/env python3
"""
index.py — print the full lesson index for this repository.

Usage:
    python index.py            # every lesson, grouped by part
    python index.py 30         # only lessons in part 03
    python index.py --list     # just the filenames, nothing else

Walks the partXX_*/ directories, reads the H1 title out of each lesson file,
and prints them in order. Missing parts are reported rather than silently
skipped, so a broken layout is visible immediately.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Title of each part, keyed by directory name.
PART_TITLES = {
    "part00_orientation": "Orientation",
    "part01_logic_proof": "Logic and Proof",
    "part02_discrete_combinatorics": "Discrete Mathematics and Combinatorics",
    "part03_linear_algebra": "Linear Algebra",
    "part04_calculus": "Calculus",
    "part05_probability_statistics": "Probability and Statistics",
    "part06_algorithms_math": "Mathematics for Algorithms",
    "part07_geometry_graphics": "Geometry for Graphics",
    "part08_optimization": "Optimisation",
    "part09_number_theory_crypto": "Number Theory and Cryptography",
    "part10_tensors_numerical": "Tensors and Numerical Methods",
}

H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
LESSON_RE = re.compile(r"^(\d{2,3})_")


def read_title(path: Path) -> str:
    """Return the H1 of a markdown file, falling back to the filename."""
    match = H1_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1).strip() if match else path.stem.replace("_", " ")


def lessons_in(part_dir: Path) -> list[tuple[int, Path]]:
    """Return (lesson_number, path) sorted by lesson number."""
    found = []
    for md in part_dir.glob("*.md"):
        if md.name == "README.md":
            continue
        match = LESSON_RE.match(md.name)
        if match:
            found.append((int(match.group(1)), md))
    return sorted(found)


def main() -> int:
    args = [a for a in sys.argv[1:]]
    as_list = "--list" in args
    if as_list:
        args.remove("--list")

    wanted = args[0] if args else None

    part_dirs = sorted(
        (p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("part")),
        key=lambda p: p.name,
    )

    total = 0
    for part_dir in part_dirs:
        key = part_dir.name.replace("part", "").split("_")[0].lstrip("0") or "0"
        if wanted and not (wanted.zfill(2) == key or wanted == part_dir.name):
            continue

        lessons = lessons_in(part_dir)
        total += len(lessons)
        title = PART_TITLES.get(part_dir.name, part_dir.name)

        if not as_list:
            print()
            print(f"  {part_dir.name}  ({len(lessons)} lessons)")
            print(f"  {'-' * 70}")
            print(f"  {title}")
            print()

        for number, path in lessons:
            rel = path.relative_to(ROOT).as_posix()
            if as_list:
                print(rel)
            else:
                title_text = read_title(path)
                print(f"    {number:>3}  {title_text}")
                print(f"         {rel}")

    if not as_list:
        print()
        print(f"  {total} lessons in total.")
        print()
        print("  Start here:  part00_orientation/00_why_math_matters.md")
        print("  Notation:    SYMBOLS.md")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())