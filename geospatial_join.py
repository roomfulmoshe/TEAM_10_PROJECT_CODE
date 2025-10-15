import pandas as pd
import geopandas as gpd

# --- TUNABLE PARAMETER ---
# Set the minimum overlap threshold. A value of 0.01 means we discard any
# tract that covers less than 1% of the taxi zone's area.
MIN_APPORTION_THRESHOLD = 0.01

print("Step 1: Loading shapefiles...")
fp_zones = 'taxi_zones/taxi_zones.shp'
fp_tracts = 'nyc_tracts/nyct2020.shp'
projected_crs = 'EPSG:2263'

try:
    zones_raw = gpd.read_file(fp_zones)
    tracts = gpd.read_file(fp_tracts).to_crs(projected_crs)
except Exception as e:
    print(f"Error loading shapefiles: {e}")
    exit()

print("\nStep 2: Cleaning the Taxi Zone data (Dissolving)...")
zones = zones_raw.dissolve(by='LocationID').reset_index()
zones = zones.to_crs(projected_crs)
print("Taxi zones cleaned.")

print("\nStep 3: Calculating total area for each cleaned taxi zone...")
zones['zone_total_area'] = zones.geometry.area

print("\nStep 4: Performing spatial intersection...")
intersection = gpd.overlay(
    tracts[['BoroCT2020', 'geometry']],
    zones[['LocationID', 'zone_total_area', 'geometry']],
    how='intersection'
)

print("\nStep 5: Aggregating MultiPolygon results and calculating initial weights...")
# First, sum up pieces of the same tract within the same zone (handles MultiPolygons)
intersection['intersect_area'] = intersection.geometry.area
agg_intersection = intersection.groupby(['LocationID', 'BoroCT2020', 'zone_total_area']).agg({'intersect_area': 'sum'}).reset_index()

# Calculate the initial weight based on the summed area
agg_intersection['apportion_weight'] = agg_intersection['intersect_area'] / agg_intersection['zone_total_area']

print(f"\nStep 6: Filtering out insignificant overlaps (less than {MIN_APPORTION_THRESHOLD * 100}%)...")
# --- THIS IS THE NEW FILTERING STEP ---
filtered_crosswalk = agg_intersection[agg_intersection['apportion_weight'] >= MIN_APPORTION_THRESHOLD].copy()
print(f"Removed rows with tiny weights. Kept {len(filtered_crosswalk)} significant overlaps.")

print("\nStep 7: Re-Normalizing weights to ensure they sum to 1...")
# --- THIS IS THE CRITICAL RE-NORMALIZATION STEP ---
# After filtering, the weights for a zone no longer sum to 1. We must fix this.
weight_sums = filtered_crosswalk.groupby('LocationID')['apportion_weight'].sum().to_dict()

filtered_crosswalk['apportion_weight_normalized'] = filtered_crosswalk.apply(
    lambda row: row['apportion_weight'] / weight_sums[row['LocationID']],
    axis=1
)
print("Remaining weights have been re-normalized.")

print("\nStep 8: Building and exporting the final crosswalk file...")
final_crosswalk = filtered_crosswalk[['LocationID', 'BoroCT2020', 'apportion_weight_normalized']]
final_crosswalk = final_crosswalk.rename(columns={
    'BoroCT2020': 'census_tract_id',
    'apportion_weight_normalized': 'apportion_weight'
})

output_filename = 'nyc_zone_tract_crosswalk_FINAL.csv'
final_crosswalk.to_csv(output_filename, index=False, float_format='%.6f')

print("-" * 50)
print(f"✅ Success! Your FINAL, cleaned crosswalk file is ready: {output_filename}")
print("This version has been cleaned, filtered, and weights are normalized to sum to 1.")
print("-" * 50)

# Final Validation Check:
validation_sum = final_crosswalk[final_crosswalk['LocationID'] == 241]['apportion_weight'].sum()
print(f"Final Validation: Sum of weights for LocationID 241 is now: {validation_sum:.6f}")
print("-" * 50)