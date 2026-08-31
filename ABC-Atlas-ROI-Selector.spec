from pathlib import Path
from PyInstaller.utils.hooks import collect_all

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
    "nbconvert",
    "ipywidgets",
    "ipympl",
]:

    package_datas, package_binaries, package_hiddenimports = collect_all(
        package
    )

    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_hiddenimports


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