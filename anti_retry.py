"""
anti_retry.py

Monitors Windows UI windows matching a title regex and automatically clicks
a visible and enabled "Retry" button when found.

Requires:
    pywinauto

Usage:
    python anti_retry.py
"""

import logging
import time
from typing import List, Optional

from pywinauto import Desktop
from pywinauto.controls.uiawrapper import UIAWrapper

# =========================
# Configuration
# =========================
WAIT_SECONDS: int = 10
TARGET_TITLE_REGEX: str = r"(?i).*Antigravity.*"
BUTTON_TITLE: str = "Retry"

# =========================
# Logging Setup
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# =========================
# Core Logic
# =========================
def find_matching_windows(title_regex: str) -> List[UIAWrapper]:
    """
    Find all windows matching the given title regex.

    Args:
        title_regex: Regex pattern for window titles.

    Returns:
        List of matching window wrappers.
    """
    try:
        return Desktop(backend="uia").windows(title_re=title_regex)
    except Exception as exc:
        logger.exception("Failed to retrieve windows: %s", exc)
        return []


def find_retry_button(window: UIAWrapper) -> Optional[UIAWrapper]:
    """
    Locate a visible and enabled 'Retry' button within a window.

    Args:
        window: The window to inspect.

    Returns:
        A valid button wrapper if found, otherwise None.
    """
    try:
        buttons = window.descendants(title=BUTTON_TITLE, control_type="Button")
    except Exception as exc:
        logger.warning("Failed to inspect window '%s': %s", window.window_text(), exc)
        return None

    for button in buttons:
        try:
            if button.is_visible() and button.is_enabled():
                return button
        except Exception:
            continue  # Skip problematic elements silently

    return None


def click_button(window: UIAWrapper, button: UIAWrapper) -> bool:
    """
    Attempt to click a button using invoke(), with fallback to click_input().

    Args:
        window: Parent window.
        button: Button element.

    Returns:
        True if click succeeded, False otherwise.
    """
    try:
        button.invoke()
        return True
    except Exception:
        logger.debug("invoke() failed, trying click_input fallback")

    try:
        window.set_focus()
        time.sleep(0.3)
        button.click_input()
        return True
    except Exception as exc:
        logger.error("Failed to click button: %s", exc)
        return False


def process_window(window: UIAWrapper) -> None:
    """
    Process a single window: find and click retry button if available.

    Args:
        window: Window to process.
    """
    title = window.window_text()

    button = find_retry_button(window)
    if not button:
        logger.debug("No retry button in window: '%s'", title)
        return

    logger.info("Retry button found in window: '%s'", title)

    if click_button(window, button):
        logger.info("Clicked 'Retry' successfully.")
    else:
        logger.warning("Failed to click 'Retry' in window: '%s'", title)


def monitor_loop() -> None:
    """
    Main monitoring loop.
    Continuously scans for matching windows and processes them.
    """
    logger.info(
        "Monitoring windows matching regex '%s' every %s seconds...",
        TARGET_TITLE_REGEX,
        WAIT_SECONDS,
    )

    while True:
        time.sleep(WAIT_SECONDS)

        windows = find_matching_windows(TARGET_TITLE_REGEX)

        if not windows:
            logger.debug("No matching windows found.")
            continue

        logger.info("Found %d matching window(s).", len(windows))

        for window in windows:
            try:
                process_window(window)
            except Exception:
                logger.exception("Unexpected error while processing a window")


# =========================
# Entry Point
# =========================
def main() -> None:
    """
    Entry point for script execution.
    """
    try:
        monitor_loop()
    except KeyboardInterrupt:
        logger.info("Script stopped by user.")


if __name__ == "__main__":
    main()