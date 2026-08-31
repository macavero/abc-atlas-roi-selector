from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import ttk


REPO_ROOT = Path(__file__).resolve().parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"

running_processes = []


def launch_notebook(notebook_name):
    notebook_path = NOTEBOOKS_DIR / notebook_name

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "voila",
            str(notebook_path),
        ],
        cwd=REPO_ROOT,
    )

    running_processes.append(process)


def open_roi_selector():
    launch_notebook(
        "multiple-roi-selector.ipynb"
    )


def open_region_editor():
    launch_notebook(
        "custom-region-editor.ipynb"
    )


# -----------------------------
# Main window
# -----------------------------

root = tk.Tk()

root.title(
    "ABC Atlas ROI Selector"
)

root.geometry(
    "420x250"
)

root.resizable(
    False,
    False
)


# -----------------------------
# Title
# -----------------------------

title = ttk.Label(
    root,
    text="ABC Atlas ROI Selector",
    font=("Segoe UI", 18, "bold"),
)

title.pack(
    pady=(30, 10)
)


subtitle = ttk.Label(
    root,
    text="Select a tool to open",
)

subtitle.pack(
    pady=(0, 20)
)


# -----------------------------
# Buttons
# -----------------------------

roi_button = ttk.Button(
    root,
    text="Open ROI Selector",
    command=open_roi_selector,
    width=30,
)

roi_button.pack(
    pady=8
)


editor_button = ttk.Button(
    root,
    text="Custom Region Editor",
    command=open_region_editor,
    width=30,
)

editor_button.pack(
    pady=8
)


root.mainloop()