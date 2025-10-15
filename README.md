# Geospatial Crosswalk: NYC Taxi Zones to Census Tracts

This repository contains the scripts and data necessary to create a robust "crosswalk" file that maps modern NYC Taxi Zones to their underlying 2020 Census Tracts.

The primary goal of this project is to build a reliable bridge between taxi trip data (which uses `LocationID`s) and demographic data from the US Census (which uses `GEOID`s for tracts). The final output, `nyc_zone_tract_crosswalk_FINAL.csv`, is a crucial input for any analysis that seeks to understand taxi demand in the context of neighborhood socio-economics.

---

## 🚀 Setup and Installation

To run the scripts in this repository, you need to set up a Python virtual environment and install the required libraries.

1.  **Navigate to the Project Directory:**
    Open your terminal and navigate to the root of this project folder.

2.  **Create a Virtual Environment:**
    This creates a self-contained environment named `venv` for this project.

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Environment:**

    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

4.  **Install Dependencies:**
    This command will install all the necessary libraries for geospatial processing and analysis.
    ```bash
    pip install pandas geopandas matplotlib seaborn
    ```

---

## 📁 Repository Structure & File Descriptions

The project is organized in a flat structure with the following key components:
├── images/
│ ├── 1_tracts_per_zone_distribution.png
│ ├── 2_top_20_complex_zones.png
│ └── 3_apportionment_weight_distribution.png
├── nyct2020/
│ └── nyct2020.shp (and companion files)
├── taxi_zones/
│ └── taxi_zones.shp (and companion files)
├── analyze_crosswalk.py
├── geospatial_join.py
├── nyc_zone_tract_crosswalk_FINAL.csv
├── test_crosswalk.py
└── zones_tracts.html

- **`geospatial_join.py`**: **(The Main Engine)** This is the core script. It takes the raw shapefiles from their respective folders (`nyct2020/` and `taxi_zones/`), performs a series of cleaning and validation steps, and produces the final crosswalk file.

- **`nyc_zone_tract_crosswalk_FINAL.csv`**: **(The Final Product)** This is the key deliverable. A clean CSV file with three columns: `LocationID`, `census_tract_id`, and `apportion_weight`. This file is ready for use in our downstream models.

- **`test_crosswalk.py`**: **(Validation Script)** A crucial script for quality control. It runs mathematical checks on the final CSV to ensure that all weights sum to 1.0 and that no unexpected zones are missing.

- **`analyze_crosswalk.py`**: **(Analysis Script)** This script reads the final crosswalk CSV and generates the three summary plots, saving them to the `/images` folder.

- **`zones_tracts.html`**: **(Visual Validation Tool)** An interactive, side-by-side map built with D3.js. This is incredibly useful for visually inspecting the shapefiles and confirming that our join logic makes sense. _(Note: Requires converting the shapefiles to GeoJSON first using a tool like [mapshaper.org](https://mapshaper.org))._

---

## ⚙️ Workflow & Usage

Here is the step-by-step process to reproduce the results. Run these commands from the root directory of the project.

1.  **Setup the Environment:** Follow the installation steps above to get your environment ready.

2.  **Generate the Crosswalk File:** Run the main geospatial join script.

    ```bash
    python geospatial_join.py
    ```

    This will create `nyc_zone_tract_crosswalk_FINAL.csv` in the root folder.

3.  **Validate the Output (Recommended):** Run the test script to confirm the file is mathematically sound.

    ```bash
    python test_crosswalk.py
    ```

    You should see "✅ Check Passed" messages.

4.  **Analyze the Results (Optional):** Run the analysis script to regenerate the plots.
    ```bash
    python analyze_crosswalk.py
    ```
    This will populate the `/images` folder.
