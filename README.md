Geospatial Crosswalk: NYC Taxi Zones to Census Tracts
This repository contains the scripts and data necessary to create a robust "crosswalk" file that maps modern NYC Taxi Zones to their underlying 2020 Census Tracts.

The primary goal of this project is to build a reliable bridge between taxi trip data (which uses LocationIDs) and demographic data from the US Census (which uses GEOIDs for tracts). The final output, nyc_zone_tract_crosswalk_FINAL.csv, is a crucial input for any analysis that seeks to understand taxi demand in the context of neighborhood socio-economics.

🚀 Setup and Installation
To run the scripts in this repository, you need to set up a Python virtual environment and install the required libraries.

Navigate to the Project Directory:
Open your terminal and navigate to the root of this project folder.

Create a Virtual Environment:
This creates a self-contained environment for this project.

Bash

python3 -m venv venv
Activate the Environment:

On macOS/Linux:

Bash

source venv/bin/activate
On Windows:

Bash

venv\Scripts\activate
Install Dependencies:
This command will install all the necessary libraries for geospatial processing and analysis.

Bash

pip install pandas geopandas matplotlib seaborn
📁 File Descriptions
Here is a breakdown of what each file and folder does:

File/Folder	Description
/shapefiles	Contains the raw geographic data. taxi_zones holds the official TLC boundaries, and nyct2020 holds the NYC census tract boundaries clipped to the shoreline.
geospatial_join.py	(The Main Engine) This is the core script. It takes the raw shapefiles, performs a series of cleaning operations (dissolving, filtering, normalizing), and runs the spatial intersection to produce the final crosswalk file.
nyc_zone_tract_crosswalk_FINAL.csv	(The Final Product). This is the key deliverable. A clean CSV file with three columns: LocationID, census_tract_id, and apportion_weight. This file is ready for use in our downstream models.
test_crosswalk.py	(Validation Script) A crucial script for quality control. It runs mathematical checks on the final CSV to ensure that all weights sum to 1.0 and that no unexpected zones are missing.
analyze_crosswalk.py	(Analysis Script) This script reads the final crosswalk CSV and generates the three summary plots stored in the /images folder, providing key insights into the geographic relationships.
/images	Contains the output plots from our analysis, which help visualize the complexity and reliability of our crosswalk file.
zones_tracts.html	(Visual Validation Tool) An interactive, side-by-side map built with D3.js. This is incredibly useful for visually inspecting the shapefiles and confirming that our join logic makes sense in complex areas.

Export to Sheets
⚙️ Workflow & Usage
Here is the step-by-step process to reproduce the results and use the tools:

Setup the Environment: Follow the installation steps above to get your environment ready.

Generate the Crosswalk File: Run the main script. This can take up to a minute.

Bash

python geospatial_join.py
This will create the nyc_zone_tract_crosswalk_FINAL.csv file.

Validate the Output (Recommended): Run the test script to confirm the file is mathematically sound.

Bash

python test_crosswalk.py
You should see "✅ Check Passed" messages.

Analyze the Results (Optional): Run the analysis script to regenerate the plots.

Bash

python analyze_crosswalk.py
This will populate the /images folder.

Visually Explore (Optional): To use the interactive map, you first need to convert the shapefiles to GeoJSON format using a tool like mapshaper.org. Once you have the .json files, open zones_tracts.html in any web browser.
