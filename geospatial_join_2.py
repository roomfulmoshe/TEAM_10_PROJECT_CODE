import pandas as pd
import geopandas as gpd

print("Step 1: Loading shapefiles...")
fp_zones = 'taxi_zones.shp'
fp_tracts = 'nyct2020.shp'
projected_crs = 'EPSG:2263'

try:
    zones_raw = gpd.read_file(fp_zones)
    tracts = gpd.read_file(fp_tracts).to_crs(projected_crs)
except Exception as e:
    print(f"Error loading shapefiles: {e}")
    exit()

print("\nStep 2: Cleaning the Taxi Zone data (Dissolving)...")
# This is the FIX for PROBLEM #2.
# We merge any messy, overlapping polygons that share the same LocationID.
zones = zones_raw.dissolve(by='LocationID').reset_index()
zones = zones.to_crs(projected_crs)
print("Taxi zones cleaned and projected.")


print("\nStep 3: Calculating total area for each cleaned taxi zone...")
zones['zone_total_area'] = zones.geometry.area


print("\nStep 4: Performing the spatial intersection...")
intersection = gpd.overlay(
    tracts[['BoroCT2020', 'geometry']],
    zones[['LocationID', 'zone_total_area', 'geometry']],
    how='intersection'
)
print("Intersection complete.")


print("\nStep 5: Calculating initial apportionment weights...")
intersection['intersect_area'] = intersection.geometry.area
intersection['apportion_weight'] = intersection['intersect_area'] / intersection['zone_total_area']


print("\nStep 6: Normalizing weights to ensure they sum to 1...")
# This is the FIX for PROBLEM #1.
# We calculate the actual sum of weights for each zone...
weight_sums = intersection.groupby('LocationID')['apportion_weight'].sum().to_dict()

# ...and then divide each weight by its group's sum to force it to 1.0.
intersection['apportion_weight_normalized'] = intersection.apply(
    lambda row: row['apportion_weight'] / weight_sums[row['LocationID']],
    axis=1
)
print("Weights have been normalized.")


print("\nStep 7: Building and exporting the final crosswalk file...")
# We now aggregate any MultiPolygon results to get one final row per pair.
final_crosswalk = intersection.groupby(['LocationID', 'BoroCT2020']).agg({
    'apportion_weight_normalized': 'sum'
}).reset_index()

final_crosswalk = final_crosswalk.rename(columns={
    'BoroCT2020': 'census_tract_id',
    'apportion_weight_normalized': 'apportion_weight'
})

output_filename = 'nyc_zone_tract_crosswalk_VALIDATED.csv'
final_crosswalk.to_csv(output_filename, index=False)

print("-" * 50)
print(f"✅ Success! Your VALIDATED crosswalk file is ready: {output_filename}")
print("This version has been cleaned and weights are normalized to sum to 1.")
print("-" * 50)

# Validation Check: Let's check the sum for LocationID 241
validation_sum = final_crosswalk[final_crosswalk['LocationID'] == 241]['apportion_weight'].sum()
print(f"Validation Check: Sum of weights for LocationID 241 is now: {validation_sum}")
print("-" * 50)