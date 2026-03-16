# Snapdragon Profiler automation notes

## Scope

Use this reference when the task is to launch Snapdragon Profiler, verify Android connectivity, and automate the final GUI steps if needed.

## Preflight

Before touching the GUI, verify:

1. `SnapdragonProfiler.exe` path is known
2. only one intended profiler instance is running
3. `adb devices -l` shows the phone as `device`
4. the phone is unlocked and USB debugging is authorized

If ADB is not healthy, fix that first. GUI automation should not be used to compensate for a broken device connection.

## Expected workflow

1. Launch or relaunch Snapdragon Profiler
2. Confirm the process exists
3. Inspect whether the main window is visible and focusable
4. Look for device list, attach/connect action, or menu path
5. Prefer hotkeys/menu automation if exposed
6. Fall back to pywinauto control targeting
7. Use AHK only if the UI tree is incomplete

## Common failure modes

### Multiple profiler instances

Symptoms:
- process exists twice
- hidden background instance
- no visible main window

Fix:
- terminate duplicates
- relaunch one clean instance

### Device appears in Windows but not in ADB

Meaning:
- MTP works, debugging does not

Fix:
- enable USB debugging
- authorize the computer
- switch USB mode if needed
- restart `adb`

### Device is `offline`

Meaning:
- ADB sees the device but authorization/handshake is incomplete

Fix:
- revoke USB debugging authorizations
- reconnect cable
- accept trust prompt again
- restart `adb`

### Profiler window exists but controls are not inspectable

Meaning:
- UI may be custom-rendered or partially accessible

Fix:
- inspect top-level window only
- try keyboard shortcuts / menus
- consider AHK fallback

## Automation strategy recommendation

Preferred order:
1. shell + adb preflight
2. pywinauto inspection
3. pywinauto action on semantic controls
4. keyboard shortcut fallback
5. AHK coordinate fallback

Bundled helpers:
- `scripts/adb_preflight.py`
- `scripts/pywinauto_probe.py`

## What to capture after a successful run

- exact exe path used
- whether multiple instances needed cleanup
- whether device detection required adb restart
- whether connect was accessible via UIA, menu, or coordinates
- any timing delays needed before the window became interactive
