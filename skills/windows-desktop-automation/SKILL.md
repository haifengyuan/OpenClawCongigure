---
name: windows-desktop-automation
description: Control and troubleshoot native Windows desktop applications when browser automation is not enough. Use when Codex/OpenClaw needs to launch, focus, inspect, click through, or script GUI workflows in Windows apps such as profilers, editors, installers, device tools, or settings panels. Especially useful for repetitive GUI sequences, local desktop apps without APIs, and bridging gaps between command-line setup and final in-app clicks.
---

# Windows Desktop Automation

Use this skill to handle native Windows GUI applications that cannot be driven through browser automation or simple shell commands.

## Quick start

1. Confirm the task is really a **Windows desktop GUI** task, not a browser task.
2. Prefer the lowest-friction path first:
   - launch app by path or shortcut
   - configure prerequisites by shell/CLI
   - use app-specific CLI or config file if available
3. If GUI interaction is still required, choose an automation stack:
   - `pywinauto` for standard Win32/UIA apps
   - PowerShell + UIAutomation when Python is unavailable or a lightweight probe is enough
   - AutoHotkey for coordinate/hotkey fallback when accessibility trees are weak
4. Build the smallest reproducible flow first: open window -> locate target control -> invoke one action.
5. Add retries, focus recovery, and screenshots/logging before scaling up.

## Decision guide

### Use this skill when

- The target is a **native Windows app**.
- The last manual steps are trapped in a GUI.
- CLI setup already works, but a few buttons/menus still need automation.
- The app exposes a stable accessibility tree or predictable hotkeys.
- The goal is deterministic repetition, not exploratory clicking.

### Do not use this skill when

- A browser tool can already control the workflow.
- The app exposes a usable CLI, config file, or API that avoids GUI automation.
- The task requires high-trust desktop takeover but no Windows automation runtime is installed yet.
- The workflow depends on fast-moving pixels, 3D viewports, or custom-rendered controls with no accessibility info; in that case expect AHK/image-based fallback and higher fragility.

## Recommended automation stack

### 1. pywinauto — default choice

Use first for most Windows desktop apps.

Best for:
- standard dialogs
- menu items
- buttons, checkboxes, text boxes, combo boxes
- window discovery and focusing
- UIA/Win32 tree inspection

Strengths:
- semantic control targeting
- more stable than coordinate clicking
- good Python ecosystem

Weaknesses:
- struggles with some GPU/custom-rendered apps
- may need backend switching (`uia` vs `win32`)

### 2. PowerShell + UIAutomation — lightweight probe path

Use for:
- quick local inspection
- basic automation without building a full Python harness
- environments where PowerShell is easier to deploy than Python packages

Strengths:
- already present on most Windows machines
- good for process/window checks and simple scripted flows

Weaknesses:
- less ergonomic than Python
- UI automation coverage varies by available assemblies/modules

### 3. AutoHotkey — fallback path

Use when:
- accessibility tree is poor or missing
- hotkeys are stable
- the app only responds reliably to focus + keyboard/mouse events

Strengths:
- pragmatic fallback
- excellent for hotkeys, focus juggling, and simple repetitive flows

Weaknesses:
- more fragile
- coordinate-based automation breaks under DPI/layout changes
- harder to maintain than semantic targeting

## Workflow

### Step 1: classify the app

Check which bucket the app falls into:

- **UIA-friendly desktop app** -> start with `pywinauto`
- **Win32-heavy older app** -> try `pywinauto` with `win32` backend
- **Custom-rendered / profiler / game tool** -> expect partial UIA coverage; prepare AHK fallback
- **Electron app** -> may expose mixed accessibility; still try `pywinauto` first

If unsure, inspect first instead of guessing.

### Step 2: stabilize prerequisites outside the GUI

Before automating clicks, handle everything you can via shell:

- launch the app
- verify process exists
- connect devices via CLI (`adb`, SDK tools, etc.)
- prepare files/paths/config
- close duplicate instances if they confuse automation

This keeps GUI automation small and less brittle.

### Step 3: inspect the window tree

Use a small probe to answer:

- what is the window title/class?
- does the control appear in UIA?
- is the target action accessible by menu/hotkey?
- does focus drift between startup and ready state?

If the control tree is visible, prefer semantic selectors.
If not, fall back to hotkeys or coordinate automation.

### Step 4: script the smallest working action

Start with one reliable action only:

- connect button
- open menu item
- select device
- start capture

Do not automate the whole workflow until one atomic step is proven stable.

### Step 5: harden the flow

Add:

- wait for window readiness
- retries for focus loss
- explicit timeouts
- visible logging
- cleanup / relaunch path

### Step 6: document the fragile parts

Record:

- exact executable path
- required privileges
- backend used (`uia` / `win32` / AHK)
- known unstable controls
- fallback hotkeys
- DPI / monitor assumptions

## Design rules

- Prefer **semantic control selection** over screen coordinates.
- Prefer **keyboard shortcuts** over mouse clicks when the shortcut is stable.
- Keep flows **short and composable**.
- Assume windows can start hidden, minimized, or behind another app.
- Expect race conditions during startup; always wait for readiness.
- For custom-rendered tools, separate what CLI can solve from what GUI must solve.
- Never assume a successful process launch means the window is interactable.

## Common patterns

### Pattern: CLI + GUI bridge

Use when the CLI can do setup but not the last GUI action.

Example:
1. Launch Snapdragon Profiler from shell.
2. Use `adb` to ensure the phone is in `device` state.
3. Bring Profiler to foreground.
4. Locate device list / connect button.
5. Click `Connect` or use the equivalent hotkey.

### Pattern: recover from invisible startup

Use when a process exists but no window is obvious.

1. Detect duplicate processes.
2. Try focus/restore on the main window.
3. If no visible window, terminate duplicates.
4. Relaunch cleanly.
5. Re-inspect the window tree.

### Pattern: custom-rendered app fallback

Use when controls are not exposed through UIA.

1. Use UIA only for top-level window detection.
2. Switch to hotkeys if the app supports them.
3. Use AHK coordinate clicks only after fixing DPI/window position.
4. Keep the scripted region minimal.

## Snapdragon Profiler notes

Snapdragon Profiler is a good example of a mixed workflow:

- launching the app is easy from shell
- device readiness should be solved with `adb`
- final attach/connect may still require GUI interaction
- the app may expose only part of its controls to automation, so inspect first before committing to `pywinauto`

For this app specifically:
- verify `adb devices -l` shows the phone as `device`
- avoid multiple profiler instances when testing automation
- try menu/hotkey routes before coordinate clicking
- expect custom UI controls and partial accessibility

## References

Read these only when needed:

- `references/stack-selection.md` — choose between pywinauto, PowerShell, and AutoHotkey
- `references/snapdragon-profiler.md` — Snapdragon Profiler automation strategy and pitfalls

## Resource plan

This skill should eventually include:

### scripts/

Add only scripts that proved repeatedly useful, for example:
- a window inspection helper
- a focus/restore helper
- a pywinauto probe for listing controls
- an ADB preflight checker for Android profiling apps

Current bundled scripts:
- `scripts/adb_preflight.py` — verify Android device readiness through `adb devices -l`
- `scripts/pywinauto_probe.py` — connect to a target window by title or PID and dump a bounded control tree (requires `pywinauto`)

### references/

Keep stack-specific notes and app-specific playbooks here.

Delete placeholder/example files once real resources replace them.
