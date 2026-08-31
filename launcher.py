from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import ttk


REPO_ROOT = Path(__file__).resolve().parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"

running_processes = []


# --------------------------------------------------
# Run Voilà internally
# --------------------------------------------------

def run_voila(notebook_path):
    """
    Run Voilà instead of opening the launcher GUI.
    """

    from voila.app import Voila

    sys.argv = [
        "voila",
        str(notebook_path),
    ]

    Voila.launch_instance()


# --------------------------------------------------
# Launch notebook
# --------------------------------------------------

def launch_notebook(notebook_name):

    notebook_path = NOTEBOOKS_DIR / notebook_name

    # Running from PyInstaller executable
    if getattr(sys, "frozen", False):

        command = [
            sys.executable,
            "--voila",
            str(notebook_path),
        ]

    # Running normally with Python
    else:

        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--voila",
            str(notebook_path),
        ]

    process = subprocess.Popen(
        command,
        cwd=REPO_ROOT,
    )

    running_processes.append(
        process
    )


def open_roi_selector():

    launch_notebook(
        "multiple-roi-selector.ipynb"
    )


def open_region_editor():

    launch_notebook(
        "custom-region-editor.ipynb"
    )


# --------------------------------------------------
# Check for Voilà mode FIRST
# --------------------------------------------------

if (
    len(sys.argv) >= 3
    and sys.argv[1] == "--voila"
):

    notebook_path = Path(
        sys.argv[2]
    )

    run_voila(
        notebook_path
    )

    sys.exit()


# --------------------------------------------------
# Launcher GUI
# --------------------------------------------------

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