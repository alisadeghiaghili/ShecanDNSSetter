"""
OS-level privilege utilities.
Kept separate so the rest of the project stays platform-agnostic.
"""

import sys
import ctypes


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin() -> None:
    """Re-launch the current process with UAC elevation and exit."""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit(0)


def ensure_admin() -> None:
    """Call at startup — re-launches with elevation if not already admin."""
    if not is_admin():
        relaunch_as_admin()
