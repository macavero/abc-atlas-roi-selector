import json
import shutil
import tempfile
import zipfile

from datetime import datetime
from pathlib import Path

from ccf_roi_selector.paths import (
    get_user_data_root,
    ensure_custom_mask_storage,
    ensure_plan_storage,
)


def export_user_data(destination_zip):

    user_root = get_user_data_root()

    ensure_custom_mask_storage()
    ensure_plan_storage()

    destination_zip = Path(destination_zip)

    with tempfile.TemporaryDirectory() as tmp:

        export_root = (
            Path(tmp)
            / "ABC-Atlas-ROI-Data"
        )

        export_root.mkdir()

        # Manifest
        manifest = {
            "format_version": 1,
            "application": "ABC Atlas ROI Selector",
            "exported": datetime.now().isoformat(
                timespec="seconds"
            ),
        }

        with open(
            export_root / "manifest.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                manifest,
                f,
                indent=4
            )

        # Custom mask registry
        registry = (
            user_root
            / "config"
            / "custom_masks.json"
        )

        if registry.exists():

            config_dir = export_root / "config"

            config_dir.mkdir()

            shutil.copy2(
                registry,
                config_dir / "custom_masks.json"
            )

        # Masks
        masks_dir = (
            user_root
            / "data"
            / "custom_masks"
        )

        if masks_dir.exists():

            shutil.copytree(
                masks_dir,
                export_root / "custom_masks"
            )

        # Plans
        plans_dir = (
            user_root
            / "plans"
        )

        if plans_dir.exists():

            shutil.copytree(
                plans_dir,
                export_root / "plans"
            )

        # Create ZIP
        with zipfile.ZipFile(
            destination_zip,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for file in export_root.rglob("*"):

                if file.is_file():

                    zip_file.write(
                        file,
                        file.relative_to(
                            export_root.parent
                        )
                    )

def import_user_data(source_zip):
    """
    Import custom masks and ROI plans from an exported ZIP.

    Existing files are preserved.
    """

    source_zip = Path(source_zip)

    user_root = get_user_data_root()

    ensure_custom_mask_storage()
    ensure_plan_storage()

    imported = 0
    skipped = 0

    with tempfile.TemporaryDirectory() as tmp:

        temp_root = Path(tmp)

        # -----------------------------
        # Extract ZIP
        # -----------------------------

        with zipfile.ZipFile(
            source_zip,
            "r"
        ) as zip_file:

            zip_file.extractall(
                temp_root
            )

        export_root = (
            temp_root
            / "ABC-Atlas-ROI-Data"
        )

        # -----------------------------
        # Validate export
        # -----------------------------

        manifest = (
            export_root
            / "manifest.json"
        )

        if not manifest.exists():

            raise ValueError(
                "This is not a valid "
                "ABC Atlas ROI data export."
            )

        # -----------------------------
        # Import plans
        # -----------------------------

        imported_plans = (
            export_root
            / "plans"
        )

        user_plans = (
            user_root
            / "plans"
        )

        if imported_plans.exists():

            for source in imported_plans.glob("*.json"):

                destination = (
                    user_plans
                    / source.name
                )

                if destination.exists():

                    skipped += 1
                    continue

                shutil.copy2(
                    source,
                    destination
                )

                imported += 1

        # -----------------------------
        # Import custom masks
        # -----------------------------

        imported_masks = (
            export_root
            / "custom_masks"
        )

        user_masks = (
            user_root
            / "data"
            / "custom_masks"
        )

        if imported_masks.exists():

            for source in imported_masks.glob("*.npz"):

                destination = (
                    user_masks
                    / source.name
                )

                if destination.exists():

                    skipped += 1
                    continue

                shutil.copy2(
                    source,
                    destination
                )

                imported += 1

        # -----------------------------
        # Merge custom mask registry
        # -----------------------------

        incoming_registry = (
            export_root
            / "config"
            / "custom_masks.json"
        )

        current_registry = (
            user_root
            / "config"
            / "custom_masks.json"
        )

        if incoming_registry.exists():

            with open(
                incoming_registry,
                "r",
                encoding="utf-8"
            ) as f:

                incoming = json.load(f)

            with open(
                current_registry,
                "r",
                encoding="utf-8"
            ) as f:

                current = json.load(f)

            for name, info in incoming.items():

                if name not in current:

                    current[name] = info

            with open(
                current_registry,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    current,
                    f,
                    indent=4
                )

    return imported, skipped