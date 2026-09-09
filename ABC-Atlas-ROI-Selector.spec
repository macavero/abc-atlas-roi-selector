from pathlib import Path
import sys
from PyInstaller.utils.hooks import (
    collect_all,
    collect_data_files,
    copy_metadata,
    collect_entry_point,
)

ROOT = Path(SPEC).resolve().parent

# Make the local project package importable while the spec is being evaluated.
# collect_all() runs before Analysis(), so Analysis(pathex=...) alone is not
# enough for packages that live under ./src.
for project_path in [ROOT, ROOT / "src"]:
    if project_path.exists():
        sys.path.insert(0, str(project_path))

# --------------------------------------------------
# Data files from our project
# --------------------------------------------------

datas = [
    (str(ROOT / "notebooks"), "notebooks"),
    (str(ROOT / "config"), "config"),
    (str(ROOT / "assets"), "assets"),
    (str(ROOT / "plans"), "plans"),
]

# Include custom masks if they already exist,
# but DO NOT package the large ABC Atlas cache.
custom_masks = ROOT / "data" / "custom_masks"

if custom_masks.exists():
    datas.append(
        (str(custom_masks), "data/custom_masks")
    )


# --------------------------------------------------
# Packages that Voilà loads dynamically
# --------------------------------------------------

hiddenimports = []
binaries = []

for package in [
    "voila",
    "jupyter_server",
    "jupyterlab_server",
    "jupyter_events",
    "jupyter_client",
    "ipykernel",
    "nbconvert",
    "nbformat",
    "ipywidgets",
    "jupyterlab_widgets",
    "widgetsnbextension",
    "comm",
    "ipympl",
    "matplotlib_inline",
    "rfc3987_syntax",
    "debugpy",

    # Local application package. Imports inside notebooks are invisible to
    # PyInstaller static analysis, so bundle every ccf_roi_selector submodule.
    "ccf_roi_selector",

    # Imported by the notebooks themselves. PyInstaller cannot discover
    # imports that live only inside .ipynb files, so collect them explicitly.
    "numpy",
    "pandas",
    "matplotlib",
    "SimpleITK",
    "abc_atlas_access",
]:

    package_datas, package_binaries, package_hiddenimports = collect_all(
        package
    )

    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_hiddenimports


# --------------------------------------------------
# Jupyter frontend assets
# --------------------------------------------------
#
# ipywidgets and ipympl have two sides:
#   1. Python packages used by the kernel
#   2. JavaScript assets used by the browser
#
# On the development computer, Jupyter can find these files in the local
# Python installation. On a computer that only has the packaged app, those
# files must be inside the PyInstaller bundle as share/jupyter/... .

jupyter_share = Path(sys.prefix) / "share" / "jupyter"

frontend_assets = [
    # ipywidgets frontend
    "labextensions/@jupyter-widgets/jupyterlab-manager",
    "nbextensions/jupyter-js-widgets",

    # ipympl / matplotlib widget frontend
    "labextensions/jupyter-matplotlib",
    "nbextensions/jupyter-matplotlib",

    # Voilà shared templates/static configuration, when installed here
    "voila",
]

for relative_path in frontend_assets:
    source = jupyter_share / relative_path

    if source.exists():
        datas.append(
            (
                str(source),
                f"share/jupyter/{relative_path}",
            )
        )
        print(f"Including Jupyter frontend asset: {source}")
    else:
        print(f"Jupyter frontend asset not found: {source}")


# Additional package data that has caused dynamic-loading issues in frozen
# Jupyter applications.
datas += collect_data_files(
    "rfc3987_syntax"
)

datas += collect_data_files(
    "jupyter_events"
)


# --------------------------------------------------
# Jupyter Client distribution metadata / entrypoints
# --------------------------------------------------

datas += copy_metadata(
    "jupyter_client"
)

# Matplotlib discovers the Jupyter inline/widget backends through
# distribution entry-point metadata. Include that metadata explicitly
# so the frozen app recognizes both backends on another computer.
datas += copy_metadata("matplotlib-inline")
datas += copy_metadata("ipympl")
datas += copy_metadata("ipywidgets")
datas += copy_metadata("jupyterlab_widgets")
datas += copy_metadata("widgetsnbextension")
datas += copy_metadata("comm")

entrypoint_datas, entrypoint_hiddenimports = collect_entry_point(
    "jupyter_client.kernel_provisioners"
)

datas += entrypoint_datas
hiddenimports += entrypoint_hiddenimports

hiddenimports += [
    "jupyter_client.provisioning",
    "jupyter_client.provisioning.local_provisioner",
    "ipykernel_launcher",
    "ipykernel.kernelapp",
]


# --------------------------------------------------
# PyInstaller analysis
# --------------------------------------------------

a = Analysis(
    ["launcher.py"],

    pathex=[
        str(ROOT),
        str(ROOT / "src"),
    ],

    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],

    noarchive=False,
)


pyz = PYZ(
    a.pure
)


exe = EXE(
    pyz,
    a.scripts,

    [],

    exclude_binaries=True,

    name="ABC-Atlas-ROI-Selector",

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,
    upx=True,

    # Keep the console visible while testing portability so that Voilà/Jupyter
    # errors are visible. Change this to False only after the portable build
    # is confirmed to work on a clean computer.
    console=True,

    icon=str(
        ROOT
        / "assets"
        / "ico_selector.ico"
    ),
)


coll = COLLECT(
    exe,
    a.binaries,
    a.datas,

    strip=False,
    upx=True,

    upx_exclude=[],

    name="ABC-Atlas-ROI-Selector",
)
