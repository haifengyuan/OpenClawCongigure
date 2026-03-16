# Stack selection

## Goal

Choose the least fragile Windows desktop automation approach for the target app.

## Selection order

1. **Avoid GUI automation entirely** if CLI/config/API can solve it.
2. **Use pywinauto** if controls are exposed through UIA or Win32.
3. **Use PowerShell probes** for process/window checks and simple verification.
4. **Use AutoHotkey** only when semantic automation is weak and hotkeys/coordinates are the only reliable path.

## pywinauto

Use when:
- the app has standard controls
- you need window/control discovery
- you want maintainable selectors

Try:
- backend `uia` first for modern apps
- backend `win32` for older dialogs/apps

Typical tasks:
- focus a window
- click a button by name
- select a menu item
- inspect descendants

Bundled helper:
- `scripts/pywinauto_probe.py` for first-pass inspection by title or PID

## PowerShell probes

Use when:
- you need to verify launch state
- you need process/path/window-title checks
- you want a small helper without packaging a full Python tool first

Typical tasks:
- list processes
- detect duplicate instances
- launch app by shortcut/exe
- pair with adb/device checks

## AutoHotkey

Use when:
- controls are custom-rendered
- hotkeys are stable
- coordinate clicking is acceptable after pinning layout/DPI

Guardrails:
- avoid absolute coordinates unless the window position is fixed
- restore/focus the window before sending input
- record monitor scale assumptions
- keep fallback flows short

## Reliability ladder

Most reliable -> least reliable:
1. app CLI / config / API
2. semantic UIA control targeting
3. window focus + hotkeys
4. coordinate clicking
5. image matching over a dynamic desktop

## What to document after success

- executable path
- required privileges
- selected automation stack
- control names or hotkeys used
- waits/timeouts needed
- known failure modes
