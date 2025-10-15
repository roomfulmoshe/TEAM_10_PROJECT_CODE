import pandas as pd
import geopandas as gpd
crosswalk_df = pd.read_csv('nyc_zone_tract_crosswalk_FINAL.csv')
zone_sums = crosswalk_df.groupby('LocationID')['apportion_weight'].sum()

# Check if any sums are far from 1.0
# A small tolerance handles tiny floating-point math differences.
if not zone_sums.between(0.99999, 1.00001).all():
    print("Warning: Not all zones sum to 1. Review these zones:")
    print(zone_sums[~zone_sums.between(0.99999, 1.00001)])
else:
    print("✅ Check Passed: All LocationID weights correctly sum to 1.0.")
    
    
all_zones = gpd.read_file('taxi_zones.shp')
zones_in_crosswalk = crosswalk_df['LocationID'].unique()
missing_zones = set(all_zones['LocationID']) - set(zones_in_crosswalk)

if not missing_zones:
    print("✅ Check Passed: No LocationIDs are missing from the crosswalk file.")
else:
    print(f"Warning: The following {len(missing_zones)} LocationIDs are missing:")
    print(missing_zones)
    
crosswalk_df = pd.read_csv('nyc_zone_tract_crosswalk_FINAL.csv')
all_zones = gpd.read_file('taxi_zones.shp')
zones_in_crosswalk = crosswalk_df['LocationID'].unique()
missing_zones = set(all_zones['LocationID']) - set(zones_in_crosswalk)

if not missing_zones:
    print("✅ Check Passed: No LocationIDs are missing.")
else:
    print(f"Info: The following {len(missing_zones)} LocationIDs are missing (as expected):")
    print(missing_zones)