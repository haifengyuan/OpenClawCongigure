#!/usr/bin/env python3
"""Probe a Windows desktop app with pywinauto.

Usage examples:
  python pywinauto_probe.py --title "Snapdragon Profiler"
  python pywinauto_probe.py --pid 42516
  python pywinauto_probe.py --title "Snapdragon Profiler" --depth 2 --backend uia

Outputs:
- match summary
- top-level window info
- descendant control tree (bounded depth)

Notes:
- Requires pywinauto to be installed.
- Try backend `uia` first, then `win32` for older apps.
"""

from __future__ import annotations

import argparse
import sys
from typing import Iterable


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--title", help="Regex/title hint for the target window")
    p.add_argument("--pid", type=int, help="Target process id")
    p.add_argument("--backend", choices=["uia", "win32"], default="uia")
    p.add_argument("--depth", type=int, default=2, help="Max descendant depth to print")
    p.add_argument("--limit", type=int, default=200, help="Max controls to print")
    return p.parse_args()


def import_pywinauto():
    try:
        from pywinauto import Application  # type: ignore
    except Exception as exc:
        eprint("PYWINAUTO_IMPORT_FAILED")
        eprint(repr(exc))
        raise
    return Application


def safe_text(value: object) -> str:
    try:
        text = str(value)
    except Exception:
        return "<unprintable>"
    return text.replace("\n", " ").strip()


def describe(wrapper) -> str:
    parts = []
    try:
        parts.append(f"text={safe_text(wrapper.window_text())!r}")
    except Exception:
        pass
    try:
        parts.append(f"class={safe_text(wrapper.class_name())!r}")
    except Exception:
        pass
    try:
        parts.append(f"ctrl={safe_text(wrapper.friendly_class_name())!r}")
    except Exception:
        pass
    try:
        rect = wrapper.rectangle()
        parts.append(f"rect=({rect.left},{rect.top},{rect.right},{rect.bottom})")
    except Exception:
        pass
    try:
        parts.append(f"visible={wrapper.is_visible()}")
    except Exception:
        pass
    try:
        parts.append(f"enabled={wrapper.is_enabled()}")
    except Exception:
        pass
    return ", ".join(parts)


def walk(wrapper, max_depth: int, limit: int) -> Iterable[str]:
    count = 0

    def _walk(node, depth: int):
        nonlocal count
        if count >= limit:
            return
        indent = "  " * depth
        try:
            line = f"{indent}- {describe(node)}"
        except Exception as exc:
            line = f"{indent}- <describe failed: {exc!r}>"
        yield line
        count += 1
        if depth >= max_depth or count >= limit:
            return
        try:
            children = node.children()
        except Exception:
            children = []
        for child in children:
            yield from _walk(child, depth + 1)
            if count >= limit:
                return

    yield from _walk(wrapper, 0)


def main() -> int:
    args = parse_args()
    if not args.title and not args.pid:
        eprint("Provide --title or --pid")
        return 2

    Application = import_pywinauto()
    app = None

    if args.pid:
        app = Application(backend=args.backend).connect(process=args.pid, timeout=10)
        wins = app.windows()
    else:
        app = Application(backend=args.backend).connect(title_re=args.title, timeout=10)
        wins = app.windows(title_re=args.title)

    print(f"BACKEND={args.backend}")
    print(f"WINDOW_COUNT={len(wins)}")
    if not wins:
        print("NO_WINDOWS_FOUND")
        return 1

    main = wins[0]
    print("MAIN_WINDOW")
    print(describe(main))
    print("CONTROL_TREE")
    for line in walk(main, args.depth, args.limit):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
