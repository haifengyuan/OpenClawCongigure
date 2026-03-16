#!/usr/bin/env python3
"""ADB preflight helper for Windows desktop profiling workflows.

Purpose:
- verify adb exists
- print connected devices with status
- make it easy to check whether a phone is ready before GUI automation
"""

from __future__ import annotations

import shutil
import subprocess
import sys


def run(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    adb = shutil.which("adb")
    if not adb:
        print("ADB_NOT_FOUND")
        return 2

    print(f"ADB={adb}")
    code, out, err = run([adb, "devices", "-l"])
    if out:
        print(out.strip())
    if err:
        print(err.strip(), file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
