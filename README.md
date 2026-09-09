# ABC Atlas ROI Selector

**ABC Atlas ROI Selector** is an interactive tool for selecting, grouping, coloring, and creating custom regions of interest (ROIs) in the Allen Mouse Brain Common Coordinate Framework (CCF).

The project provides a graphical interface for working with anatomical regions without requiring users to manually edit Python code.

It includes two main tools:

- **Multiple ROI Selector** — select, group, color, save, import, export, and visualize anatomical regions.
- **Custom Region Editor** — draw and save custom anatomical regions across Allen Atlas plates.

---

## Features

### Multiple ROI Selector

The Multiple ROI Selector supports:

- Allen CCF anatomical regions
- Composite regions defined in `config/custom_regions.json`
- Manually curated custom masks
- Multiple ROIs in the same visualization
- Multiple anatomical regions grouped into a single ROI
- Custom display colors for each ROI
- Saving ROI configurations as reusable plans
- Loading previously saved ROI plans
- Exporting ROI plans for sharing or transfer
- Importing previously exported ROI plans
- Interactive navigation through Allen Atlas plates

Each ROI can contain one or more anatomical regions. Regions assigned to the same ROI are displayed using the same selected color.

The viewer is loaded only after the user confirms the selected regions.

### Custom Region Editor

The Custom Region Editor allows users to create anatomical regions that are not directly represented by a single Allen CCF annotation.

It supports:

- Drawing polygon-based regions directly on Allen Atlas plates
- Building one custom region across multiple atlas plates
- Adding multiple polygons to the same plate
- Optionally restricting drawing to an existing Allen CCF or composite region
- Undoing drawing points
- Clearing individual plates
- Clearing the entire region
- Saving custom regions as compressed 3D masks

Saved custom regions can then be selected in the Multiple ROI Selector alongside standard Allen CCF regions.

---

## Windows Application

A packaged Windows version of ABC Atlas ROI Selector is distributed through **GitHub Releases**.

The packaged application does not require the user to install Python separately.

### Installation

1. Go to the **Releases** section of this repository.
2. Download the latest Windows `.zip` release.
3. Extract the entire ZIP file.
4. Open the extracted folder.
5. Run:

   `ABC-Atlas-ROI-Selector.exe`

> **Important:** Keep the executable together with the other files and folders included in the extracted application directory. The executable depends on these bundled resources.

---

## Running from Source

The source code and Jupyter notebooks are also available for development and reproducibility.

Clone the repository:

```bash
git clone https://github.com/macavero/abc-atlas-roi-selector.git
cd abc-atlas-roi-selector
```

Create or activate a Python environment, then install the project:

```bash
pip install -e .
```

Launch the application:

```bash
python launcher.py
```

The individual notebook interfaces are located in:

```text
notebooks/
├── multiple-roi-selector.ipynb
└── custom-region-editor.ipynb
```

---

## ROI Plans

ROI configurations can be saved as reusable JSON plans.

A saved plan stores information such as:

- ROI names
- Anatomical regions assigned to each ROI
- Display colors

Plans can later be loaded into the Multiple ROI Selector to reproduce a previous ROI configuration.

ROI plans can also be **exported and imported**, making it easy to share configurations between users or transfer them between computers without manually rebuilding the ROI setup.

User-generated plans are stored locally in the `plans/` directory and are not tracked by Git.

---

## Custom Regions

Custom regions are created using the **Custom Region Editor**.

A custom region is stored as a compressed 3D mask. The associated registry records information about the mask and allows it to be integrated into the ROI selection system.

Custom regions can span multiple atlas plates and can optionally be restricted to an existing Allen CCF or composite anatomical region while being drawn.

Once saved, a custom region becomes available in the Multiple ROI Selector alongside:

- Allen CCF regions
- Composite regions
- Other custom masks

This allows standard atlas annotations and manually curated regions to be combined in the same visualization.

---

## Project Structure

```text
abc-atlas-roi-selector/
│
├── assets/
│   └── ico_selector.ico
│
├── config/
│   ├── custom_masks.json
│   └── custom_regions.json
│
├── data/
│   ├── abc_atlas/
│   └── custom_masks/
│
├── notebooks/
│   ├── custom-region-editor.ipynb
│   └── multiple-roi-selector.ipynb
│
├── plans/
│   └── .gitkeep
│
├── src/
│   └── ccf_roi_selector/
│       ├── __init__.py
│       ├── atlas.py
│       ├── paths.py
│       ├── plotting.py
│       ├── roi.py
│       └── sharing.py
│
├── ABC-Atlas-ROI-Selector.spec
├── launcher.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### Main Components

`notebooks/`  
Contains the interactive interfaces for ROI selection and custom region creation.

`src/ccf_roi_selector/`  
Contains reusable Python functionality for atlas loading, file paths, ROI resolution, visualization, and sharing functionality.

`config/`  
Contains region definitions and registries used by the ROI system.

`plans/`  
Stores ROI plans created by the user.

`data/custom_masks/`  
Stores custom 3D masks created with the Custom Region Editor.

`data/abc_atlas/`  
Stores local Allen/ABC Atlas data used by the application. This directory is not tracked by Git.

---

## How Regions Are Resolved

The ROI selector combines regions from three sources:

1. **Allen CCF regions**
2. **Composite regions** defined in `config/custom_regions.json`
3. **Custom masks** registered through `config/custom_masks.json`

This allows standard atlas annotations, grouped anatomical structures, and manually defined regions to be used together in the same visualization.

---

## Technologies

The project is built with Python and uses tools including:

- NumPy
- Matplotlib
- Jupyter
- ipywidgets
- Voilà
- Allen Mouse Brain Common Coordinate Framework resources
- ABC Atlas resources
- PyInstaller

Voilà is used to provide the notebook-based graphical interfaces, while PyInstaller is used to package the application as a standalone Windows distribution.

---

## Status

ABC Atlas ROI Selector is currently under active development.

Current functionality includes:

- Multi-ROI selection
- ROI grouping
- Custom ROI colors
- Allen Atlas plate navigation
- Saving and loading ROI plans
- Importing and exporting ROI plans
- Custom polygon-based region drawing
- Multi-plate custom masks
- Integration of custom regions into ROI visualization
- Packaged Windows application

---

## Author

Created by **Camila Vergara**

GitHub: [@macavero](https://github.com/macavero)