# 🖱️ Window Retry Clicker

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

A lightweight Python automation tool that monitors Windows UI applications and automatically clicks a visible **"Retry"** button when it appears. 

Built with [`pywinauto`](https://github.com/pywinauto/pywinauto), this script is originally designed to handle "Google Antigravity" windows, but is incredibly useful for handling any flaky apps, retry dialogs, or unstable workflows that require manual intervention.

---

## ⚠️ Trademark Disclaimer

**"Google" and "Google Antigravity" are trademarks of Google LLC.** 
This project is an independent, open-source automation tool and is **not** affiliated with, authorized, maintained, sponsored, or endorsed by Google LLC or any of its affiliates. The use of any trade name or trademark is for identification and reference purposes only and does not imply any association with the trademark holder of their product brand.

---

## 🚀 Features

- 🔍 Monitors all windows matching a configurable title regex.
- 🎯 Detects **visible and enabled** "Retry" buttons only.
- ⚡ Automatically clicks using `.invoke()` with fallback to `.click_input()`.
- 🧠 Resilient to UI glitches and transient failures.
- 📜 Clean logging (no noisy console spam).
- 🧩 Modular and easy to extend.

---

## 📦 Requirements

- Python **3.8+**
- Windows OS
- `pywinauto`

Install dependencies via pip:

```bash
pip install pywinauto
```

---

## 💻 Usage

Run the script from your terminal or command prompt:

```bash
python anti_retry.py
```

Leave the script running in the background. It will wake up at the specified intervals, scan your desktop for matching windows, and automatically clear any "Retry" dialogs it encounters. Press `Ctrl+C` in the terminal to stop the script.

---

## ⚙️ Configuration

The tool is designed to be easily modified. Open `anti_retry.py` and modify the constants at the top of the file under the **Configuration** section to suit your exact needs:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `WAIT_SECONDS` | `10` | The interval (in seconds) between window scans. |
| `TARGET_TITLE_REGEX` | `r"(?i).*Antigravity.*"` | A case-insensitive Regular Expression used to match the target window's title. |
| `BUTTON_TITLE` | `"Retry"` | The exact text/title of the button the script should look for and click. |

*To target a completely different application, simply update `TARGET_TITLE_REGEX` to match that application's window title, and change `BUTTON_TITLE` if the dialog button has different text (e.g., "Reconnect", "OK", "Continue").*

---

## 🛠️ How It Works

1. **Discovery:** The script utilizes the `uia` (UIAutomation) backend of `pywinauto` to scan the Windows desktop for windows matching the provided `TARGET_TITLE_REGEX`.
2. **Inspection:** For every matching window, it searches the UI tree for a `Button` control type matching the `BUTTON_TITLE`. It verifies that the button is currently visible and enabled to prevent clicking disabled UI elements.
3. **Execution:** It attempts a background `.invoke()` to trigger the button without stealing your mouse cursor. 
4. **Fallback:** If `.invoke()` fails (which is common in complex desktop apps), it temporarily brings the window into focus and simulates a physical mouse click using `.click_input()`.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues) if you want to contribute.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is distributed under the **MIT License**. See the `LICENSE` file for more information.
