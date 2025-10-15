import pandas as pd
import geopandas as gpd

print("Step 1: Loading the taxi zone and census tract shapefiles...")

# Define the filenames for your shapefiles
# This assumes the script is in the same folder as your shapefiles.
# If not, you will need to provide the full path to the files.
fp_zones = 'taxi_zones.shp'
fp_tracts = 'nyct2020.shp'

# Use a projected Coordinate Reference System (CRS) suitable for NYC (EPSG:2263)
# This is critical for calculating area accurately in feet, not degrees.
projected_crs = 'EPSG:2263'

# Read and re-project both files at once
try:
    zones = gpd.read_file(fp_zones).to_crs(projected_crs)
    tracts = gpd.read_file(fp_tracts).to_crs(projected_crs)
    print("Shapefiles loaded and projected successfully.")
except Exception as e:
    print(f"Error loading shapefiles: {e}")
    print("Please ensure both shapefiles and all their companion files (.shx, .dbf, etc.) are in the same folder as this script.")
    exit()


print("\nStep 2: Calculating the total area of each original taxi zone...")
# This calculation must be done *before* the intersection
zones['zone_total_area'] = zones.geometry.area


print("\nStep 3: Performing the spatial intersection...")
# This is the core geoprocessing step. It creates a new layer of polygons
# representing where the census tracts and taxi zones overlap.

# Check for the correct column names before the overlay
# The taxi zone ID is 'LocationID' and the tract ID is usually 'BoroCT2020'
if 'LocationID' not in zones.columns or 'BoroCT2020' not in tracts.columns:
    print("Error: Could not find 'LocationID' or 'BoroCT2020' columns.")
    print(f"Taxi Zone columns: {zones.columns}")
    print(f"Census Tract columns: {tracts.columns}")
    print("Please check the column names in your shapefiles.")
    exit()

intersection = gpd.overlay(
    tracts[['BoroCT2020', 'geometry']],
    zones[['LocationID', 'zone_total_area', 'geometry']],
    how='intersection'
)
print("Intersection complete.")


print("\nStep 4: Calculating the apportionment weights...")
# Calculate the area of each small, intersected polygon
intersection['intersect_area'] = intersection.geometry.area

# The weight is the ratio of the intersected area to the original zone's total area
# This tells you what percentage of the taxi zone falls within that specific census tract piece.
intersection['apportion_weight'] = intersection['intersect_area'] / intersection['zone_total_area']


print("\nStep 5: Building and exporting the final crosswalk file...")
# Select and rename the columns for a clean, final CSV file
final_crosswalk = intersection[['LocationID', 'BoroCT2020', 'apportion_weight']]
final_crosswalk = final_crosswalk.rename(columns={'BoroCT2020': 'census_tract_id'})

# Define the output filename
output_filename = 'nyc_zone_tract_crosswalk.csv'

# Save the final table to a CSV file
final_crosswalk.to_csv(output_filename, index=False)

print("-" * 50)
print(f"✅ Success! Your crosswalk file has been created: {output_filename}")
print("Here's a preview of your data:")
print(final_crosswalk.head())
print("-" * 50)