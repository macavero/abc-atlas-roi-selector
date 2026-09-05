from pathlib import Path
from PyInstaller.utils.hooks import (
    collect_all,
    collect_data_files,
    copy_metadata,
    collect_entry_point,
)

ROOT = Path(SPEC).resolve().parent

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
    "ipympl",
    "rfc3987_syntax",
]:

    package_datas, package_binaries, package_hiddenimports = collect_all(
        package
    )

    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_hiddenimports

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

entrypoint_datas, entrypoint_hiddenimports = collect_entry_point(
    "jupyter_client.kernel_provisioners"
)

datas += entrypoint_datas
hiddenimports += entrypoint_hiddenimports

hiddenimports += [
    "jupyter_client.provisioning",
    "jupyter_client.provisioning.local_provisioner",
    "ipykernel_launcher",
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