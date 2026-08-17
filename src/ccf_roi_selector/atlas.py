from pathlib import Path

import SimpleITK as sitk

from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache


def load_atlas():
    # Find the root of the repository
    repo_root = Path(__file__).resolve().parents[2]

    # ABC Atlas cache location
    cache_dir = repo_root / "data" / "abc_atlas"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Connect to ABC Atlas cache
    abc_cache = AbcProjectCache.from_cache_dir(cache_dir)

    # Get CCF files
    template_file = abc_cache.get_file_path(
        directory="Allen-CCF-2020",
        file_name="average_template_25"
    )

    annotation_file = abc_cache.get_file_path(
        directory="Allen-CCF-2020",
        file_name="annotation_25"
    )

    # Read images
    template_image = sitk.ReadImage(template_file)
    annotation_image = sitk.ReadImage(annotation_file)

    # Convert to NumPy arrays
    template = sitk.GetArrayFromImage(template_image)
    annotation = sitk.GetArrayFromImage(annotation_image)

    # Load parcellation metadata
    parcellation_annotation = abc_cache.get_metadata_dataframe(
        directory="Allen-CCF-2020",
        file_name="parcellation_to_parcellation_term_membership"
    )

    return template, annotation, parcellation_annotation