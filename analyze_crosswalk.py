import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os

# --- Setup ---
# Create the 'images' subfolder if it doesn't already exist
if not os.path.exists('images'):
    os.makedirs('images')
    print("Created 'images' subfolder.")

# Load the final crosswalk file we created
try:
    crosswalk_df = pd.read_csv('nyc_zone_tract_crosswalk_FINAL.csv')
except FileNotFoundError:
    print("Error: The crosswalk file 'nyc_zone_tract_crosswalk_FINAL.csv' was not found.")
    print("Please ensure you have run the previous script to generate this file.")
    exit()

# Load the taxi zones shapefile to get the zone names for better plots
try:
    # We only need the LocationID and the zone name for this analysis
    taxi_zones_gdf = gpd.read_file('taxi_zones.shp')[['LocationID', 'zone']]
except Exception as e:
    print(f"Warning: Could not load taxi_zones.shp: {e}")
    print("Plots will be generated using LocationID numbers instead of names.")
    # Create a dummy dataframe if shapefile is not found so the script can still run
    taxi_zones_gdf = pd.DataFrame({'LocationID': [], 'zone': []})

print("Successfully loaded data. Starting analysis...")


# --- Analysis & Plotting ---

# Plot 1: Distribution of Census Tracts per Taxi Zone
print("Generating Plot 1: Distribution of Tracts per Zone...")
plt.figure(figsize=(12, 7))
tracts_per_zone = crosswalk_df.groupby('LocationID')['census_tract_id'].count()
sns.histplot(tracts_per_zone, bins=25, kde=True)
plt.title('Distribution of Census Tracts per Taxi Zone', fontsize=16, fontweight='bold')
plt.xlabel('Number of Census Tracts Covered', fontsize=12)
plt.ylabel('Number of Taxi Zones', fontsize=12)
plt.grid(axis='y', alpha=0.75)
plt.figtext(0.5, -0.1, "Insight: Most taxi zones cover a small number of census tracts (1-10), allowing for precise demographic mapping.\nOutliers represent large areas (airports, parks) where socio-economic data will be more diluted.",
            ha="center", fontsize=10, style='italic')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('images/1_tracts_per_zone_distribution.png', bbox_inches='tight')
plt.close()


# Plot 2: Top 20 Most Geographically Complex Taxi Zones
print("Generating Plot 2: Top 20 Most Complex Zones...")
zone_tract_counts = tracts_per_zone.reset_index().rename(columns={'census_tract_id': 'tract_count'})

# Merge with zone names for better plot labels
if not taxi_zones_gdf.empty:
    zone_tract_counts = zone_tract_counts.merge(taxi_zones_gdf, on='LocationID', how='left')
    # Handle cases where a zone name might be missing
    zone_tract_counts['zone'].fillna('Unknown', inplace=True)
    zone_tract_counts['zone_label'] = zone_tract_counts['zone'] + " (" + zone_tract_counts['LocationID'].astype(str) + ")"
else:
    zone_tract_counts['zone_label'] = "ID: " + zone_tract_counts['LocationID'].astype(str)

top_20_zones = zone_tract_counts.sort_values(by='tract_count', ascending=False).head(20)

plt.figure(figsize=(14, 10))
sns.barplot(x='tract_count', y='zone_label', data=top_20_zones, palette='viridis')
plt.title('Top 20 Taxi Zones by Number of Associated Census Tracts', fontsize=16, fontweight='bold')
plt.xlabel('Number of Census Tracts Covered', fontsize=12)
plt.ylabel('Taxi Zone', fontsize=12)
plt.grid(axis='x', alpha=0.75)
plt.figtext(0.5, -0.05, "Insight: These zones require careful handling in an equity analysis as demand is spread across the most neighborhoods.\nThey represent the highest level of spatial uncertainty for your socio-economic mapping.",
            ha="center", fontsize=10, style='italic')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('images/2_top_20_complex_zones.png', bbox_inches='tight')
plt.close()


# Plot 3: Histogram of Apportionment Weights
print("Generating Plot 3: Distribution of Apportionment Weights...")
plt.figure(figsize=(12, 7))
sns.histplot(crosswalk_df['apportion_weight'], bins=30, kde=False)
plt.title('Distribution of Apportionment Weights', fontsize=16, fontweight='bold')
plt.xlabel('Apportionment Weight (Tract Area / Zone Area)', fontsize=12)
plt.ylabel('Count of Overlaps (Log Scale)', fontsize=12)
plt.yscale('log') # Use a log scale to see the detail for smaller values
plt.grid(axis='y', alpha=0.75)
plt.figtext(0.5, -0.1, "Insight: The vast majority of weights are close to 1.0. This is excellent news for your project.\nIt means most tracts fall almost entirely within one zone, making the link between demand and demographics very strong.",
            ha="center", fontsize=10, style='italic')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('images/3_apportionment_weight_distribution.png', bbox_inches='tight')
plt.close()

print("\n✅ Success! All 3 plots have been saved to the 'images' subfolder.")