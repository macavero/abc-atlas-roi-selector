import numpy as np
from matplotlib.colors import to_rgba
import matplotlib.pyplot as plt

from ccf_roi_selector.roi import get_roi_indices


def create_color_overlay(annotation_slice, parcellation_annotation, roi_colors):
    """
    Create an RGBA color overlay for a single 2D annotation slice.
    """

    rgba = np.zeros(
        annotation_slice.shape + (4,),
        dtype=np.float32
    )

    for acronym, color in roi_colors.items():

        indices = get_roi_indices(
            parcellation_annotation,
            acronym
        )

        mask = np.isin(annotation_slice, indices)

        rgba[mask] = to_rgba(color)

    return rgba

def get_slice(volume, slice_index):
    """
    Extract and orient a 2D slice from axis 2.
    """

    slice_2d = volume[:, :, slice_index]

    # Keep the orientation that was working in the notebook
    slice_2d = np.rot90(slice_2d, k=3)

    return slice_2d

def show_overlay_slice(
    template,
    annotation,
    parcellation_annotation,
    roi_colors,
    slice_index,
    title=None
):
    template_slice = get_slice(template, slice_index)
    annotation_slice = get_slice(annotation, slice_index)

    overlay = create_color_overlay(
        annotation_slice,
        parcellation_annotation,
        roi_colors
    )

    plt.figure(figsize=(8, 7))

    plt.imshow(template_slice, cmap="gray")
    plt.imshow(overlay, alpha=0.7)

    if title is not None:
        plt.title(title)

    plt.axis("off")
    plt.tight_layout()
    plt.show()