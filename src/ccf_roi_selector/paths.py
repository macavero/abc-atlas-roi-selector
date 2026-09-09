import os
import sys
import shutil
from pathlib import Path


APP_NAME = "ABC-Atlas-ROI-Selector"


def get_bundled_root():
    """
    Location of files shipped with the application.
    """

    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parents[2]


def get_user_data_root():
    """
    Writable directory for user-created data.
    """

    if sys.platform == "win32":

        base = Path(
            os.environ.get(
                "LOCALAPPDATA",
                Path.home() / "AppData" / "Local"
            )
        )

    elif sys.platform == "darwin":

        base = (
            Path.home()
            / "Library"
            / "Application Support"
        )

    else:

        base = Path(
            os.environ.get(
                "XDG_DATA_HOME",
                Path.home() / ".local" / "share"
            )
        )

    root = base / APP_NAME

    root.mkdir(
        parents=True,
        exist_ok=True
    )

    return root


def ensure_custom_mask_storage():
    """
    Create writable custom-mask storage.

    Existing masks bundled with the application
    are copied there the first time.
    """

    bundled_root = get_bundled_root()
    user_root = get_user_data_root()

    user_config_dir = user_root / "config"
    user_masks_dir = user_root / "data" / "custom_masks"

    user_config_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    user_masks_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------
    # Initial registry
    # ---------------------------------

    bundled_registry = (
        bundled_root
        / "config"
        / "custom_masks.json"
    )

    user_registry = (
        user_config_dir
        / "custom_masks.json"
    )

    if not user_registry.exists():

        if bundled_registry.exists():

            shutil.copy2(
                bundled_registry,
                user_registry
            )

        else:

            user_registry.write_text(
                "{}",
                encoding="utf-8"
            )

    # ---------------------------------
    # Initial bundled masks
    # ---------------------------------

    bundled_masks_dir = (
        bundled_root
        / "data"
        / "custom_masks"
    )

    if bundled_masks_dir.exists():

        for source in bundled_masks_dir.glob("*.npz"):

            destination = (
                user_masks_dir
                / source.name
            )

            if not destination.exists():

                shutil.copy2(
                    source,
                    destination
                )

    return user_root

def ensure_plan_storage():
    """
    Create writable storage for ROI plans.

    Plans bundled with the application are copied
    to the user's data folder the first time.
    """

    bundled_root = get_bundled_root()
    user_root = get_user_data_root()

    user_plans_dir = (
        user_root
        / "plans"
    )

    user_plans_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Plans that came with the program/repository
    bundled_plans_dir = (
        bundled_root
        / "plans"
    )

    if bundled_plans_dir.exists():

        for source in bundled_plans_dir.glob("*.json"):

            destination = (
                user_plans_dir
                / source.name
            )

            # Never overwrite a user's version
            if not destination.exists():

                shutil.copy2(
                    source,
                    destination
                )

    return user_plans_dir