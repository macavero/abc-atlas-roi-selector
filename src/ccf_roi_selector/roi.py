import json
from pathlib import Path
import numpy as np
from ccf_roi_selector.paths import (
    get_bundled_root,
    ensure_custom_mask_storage,
)

def get_roi_indices(parcellation_annotation, acronym):
    """
    Return the parcellation indices associated with an ROI acronym.
    """

    rows = parcellation_annotation[
        parcellation_annotation["parcellation_term_acronym"] == acronym
    ]

    if len(rows) == 0:
        print(f"Warning: ROI '{acronym}' not found.")
        return []

    return rows["parcellation_index"].unique()

def load_custom_regions():

    bundled_root = get_bundled_root()

    config_file = (
        bundled_root
        / "config"
        / "custom_regions.json"
    )

    with open(config_file, "r") as f:
        return json.load(f)
    
def resolve_region_indices(parcellation_annotation, region):

    custom_regions = load_custom_regions()

    regions_to_find = custom_regions.get(region, [region])

    all_indices = []

    for allen_region in regions_to_find:
        indices = get_roi_indices(
            parcellation_annotation,
            allen_region
        )

        all_indices.extend(indices)

    return np.unique(all_indices)

def load_custom_masks_registry():
    """
    Load the registry of manually drawn custom masks.
    """

    user_root = ensure_custom_mask_storage()

    registry_file = (
        user_root
        / "config"
        / "custom_masks.json"
    )

    with open(
        registry_file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def load_custom_mask(region):
    """
    Load the 3D boolean mask for a manually drawn custom region.

    Returns None if the region is not a custom mask.
    """

    registry = load_custom_masks_registry()

    if region not in registry:
        return None

    user_root = ensure_custom_mask_storage()

    info = registry[region]

    mask_path = (
        user_root
        / info["file"]
    )

    mask_key = info.get(
        "mask_key",
        "mask"
    )

    data = np.load(mask_path)

    return data[mask_key].astype(bool)