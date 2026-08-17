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