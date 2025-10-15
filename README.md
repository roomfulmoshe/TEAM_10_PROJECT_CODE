Geospatial Crosswalk: NYC Taxi Zones to Census Tracts
This repository contains the scripts and data necessary to create a robust "crosswalk" file that maps modern NYC Taxi Zones to their underlying 2020 Census Tracts.

The primary goal of this project is to build a reliable bridge between taxi trip data (which uses LocationIDs) and demographic data from the US Census (which uses GEOIDs for tracts). The final output, located at data/output/nyc_zone_tract_crosswalk_FINAL.csv, is a crucial input for any analysis that seeks to understand taxi demand in the context of neighborhood socio-economics.

🚀 Setup and Installation
To run the scripts in this repository, you need to set up a Python virtual environment and install the required libraries.

Navigate to the Project Directory:
Open your terminal and navigate to the root of this project folder.

Create a Virtual Environment:
This creates a self-contained environment for this project.

python3 -m venv venv

Activate the Environment:

On macOS/Linux:

source venv/bin/activate

On Windows:

venv\Scripts\activate

Install Dependencies:
This command will install all the necessary libraries for geospatial processing and analysis.

pip install pandas geopandas matplotlib seaborn

📁 Repository Structure
The project is organized into the following directories:

├── data/
│ ├── input/
│ │ └── shapefiles/
│ │ ├── nyct2020/ # Contains the NYC Census Tracts shapefile
│ │ └── taxi_zones/ # Contains the NYC Taxi Zones shapefile
│ └── output/
│ └── nyc_zone_tract_crosswalk_FINAL.csv # The final, validated output file
├── src/
│ ├── geospatial_join.py # Main script to generate the crosswalk
│ ├── test_crosswalk.py # Script to validate the final crosswalk
│ └── analyze_crosswalk.py # Script to generate analysis plots
├── visualizations/
│ ├── images/ # Output folder for analysis plots
│ └── zones_tracts.html # Interactive map for visual validation
└── README.md # This file

⚙️ Workflow & Usage
Here is the step-by-step process to reproduce the results. Run these commands from the root directory of the project.

Setup the Environment: Follow the installation steps above to get your environment ready.

Generate the Crosswalk File: Run the main geospatial join script. It reads the shapefiles from data/input and saves the output to data/output.

python src/geospatial_join.py

Validate the Output (Recommended): Run the test script to confirm the file is mathematically sound.

python src/test_crosswalk.py

You should see "✅ Check Passed" messages confirming the file's integrity.

Analyze the Results (Optional): Run the analysis script to regenerate the plots. The plots will be saved in the visualizations/images/ directory.

python src/analyze_crosswalk.py

Key Components Explained
src/geospatial_join.py: This is the core engine of the project. It performs a multi-step process:

Loads the two shapefiles.

Cleans the taxi zone data by dissolving messy, overlapping polygons.

Performs a spatial intersection to find all areas of overlap.

Aggregates results and calculates initial apportion_weight based on area.

Filters out insignificant "sliver" overlaps (less than 1%).

Re-normalizes the remaining weights to ensure they sum perfectly to 1 for every taxi zone.

data/output/nyc_zone_tract_crosswalk_FINAL.csv: This is the final, validated product. It is a clean lookup table that is ready to be joined with any taxi or census dataset.

visualizations/zones_tracts.html: An interactive, side-by-side map built with D3.js. This tool is incredibly useful for visually inspecting the raw shapefiles and confirming that our join logic makes sense in complex areas like airports and islands. (Note: To use this, you must first convert the shapefiles to GeoJSON using a tool like mapshaper.org).
