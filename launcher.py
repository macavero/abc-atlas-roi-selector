from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import (
    ttk,
    filedialog,
    messagebox,
)

import webbrowser
from datetime import datetime

from ccf_roi_selector.sharing import (
    export_user_data,
    import_user_data,
)

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
def export_data():

    filename = (
        "ABC-Atlas-ROI-Data_"
        + datetime.now().strftime("%Y-%m-%d")
        + ".zip"
    )

    destination = filedialog.asksaveasfilename(
        title="Export ROI data",
        initialfile=filename,
        defaultextension=".zip",
        filetypes=[
            ("ZIP files", "*.zip")
        ],
    )

    if not destination:
        return

    try:

        export_user_data(
            destination
        )

        messagebox.showinfo(
            "Export complete",
            "Masks and ROI plans were exported successfully."
        )

    except Exception as error:

        messagebox.showerror(
            "Export failed",
            str(error)
        )


def import_data():

    source = filedialog.askopenfilename(
        title="Import ROI data",
        filetypes=[
            ("ABC Atlas ROI data", "*.zip")
        ],
    )

    if not source:
        return

    try:

        imported, skipped = import_user_data(
            source
        )

        messagebox.showinfo(
            "Import complete",
            (
                f"Imported: {imported}\n"
                f"Already existed: {skipped}\n\n"
                "Reopen the ROI Selector to refresh."
            )
        )

    except Exception as error:

        messagebox.showerror(
            "Import failed",
            str(error)
        )


root = tk.Tk()

root.title(
    "ABC Atlas ROI Selector"
)

root.geometry(
    "420x380"
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

separator = ttk.Separator(
    root,
    orient="horizontal"
)

separator.pack(
    fill="x",
    padx=60,
    pady=(15, 10)
)


export_button = ttk.Button(
    root,
    text="Export My Data",
    command=export_data,
    width=30,
)

export_button.pack(
    pady=5
)


import_button = ttk.Button(
    root,
    text="Import Data",
    command=import_data,
    width=30,
)

import_button.pack(
    pady=5
)

# Watermark
footer = ttk.Label(
    root,
    text="Created by Camila Vergara • GitHub: macavero",
    font=("Segoe UI", 8),
    cursor="hand2",
)

footer.pack(
    side="bottom",
    pady=(10, 8)
)

footer.bind(
    "<Button-1>",
    lambda event: webbrowser.open(
        "https://github.com/macavero"
    )
)

root.mainloop()