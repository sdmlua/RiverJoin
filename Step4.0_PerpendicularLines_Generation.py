### Before using these codes, you need to first have the nodes shapefile of your reaches (here we use SWORD reach nodes)
### If you don't have it yet, you can generate it using the 'Generate Points Along Lines' function in ArcGIS.


import geopandas as gpd
import numpy as np
from shapely.geometry import LineString, Point


## Step 1: Define the function of generating perpendicular lines of SWORD reaches based on the evenly spacing nodes along the reaches
def generate_perpendicular_line(node, previous_node, length):
    """
    Generate a line perpendicular to the segment formed by `previous_node` and `node`.
    
    Parameters:
    - node: The current shapely Point (node)
    - previous_node: The previous shapely Point (node)
    - length: Length of the perpendicular line
    
    Returns:
    A shapely LineString representing the perpendicular line.
    """
    # Extract coordinates for the two points
    x1, y1 = previous_node.x, previous_node.y
    x2, y2 = node.x, node.y
    
    # Compute the direction vector between the two nodes
    dx, dy = x2 - x1, y2 - y1
    
    # Rotate the direction vector by 90 degrees to get a perpendicular vector
    perp_dx = -dy
    perp_dy = dx
    
    # Normalize the perpendicular vector and scale it to the desired length
    norm = np.sqrt(perp_dx**2 + perp_dy**2)
    perp_dx /= norm
    perp_dy /= norm
    
    # Create the endpoints of the perpendicular line (both directions)
    perp_start = (node.x + perp_dx * length / 2, node.y + perp_dy * length / 2)
    perp_end = (node.x - perp_dx * length / 2, node.y - perp_dy * length / 2)
    
    # Return the LineString representing the perpendicular line
    return LineString([perp_start, perp_end])



## Step 2: Specify the SWORD nodes path
sword_nodes_gdf = gpd.read_file(r"path to your node file stored in a gdb or gpkg", layer = "name of node file")



## Step 3: Use the function to generate the perpendicular lines

# Create a GeoDataFrame to hold the perpendicular lines
perp_lines = []

# Iterate over each node starting from the second point (because we need a previous point)
for i in range(1, len(sword_nodes_gdf)):
    current_node = sword_nodes_gdf.geometry.iloc[i]
    previous_node = sword_nodes_gdf.geometry.iloc[i - 1]
    length=0.006   # [Specify the perpendicular lines length you want]
    
    # print(current_node, previous_node)
    print(f"node {i}/{len(sword_nodes_gdf)} is being processed...")

    # Generate the perpendicular line for the current node
    perp_line = generate_perpendicular_line(current_node, previous_node, length)
    
    # Store the perpendicular line
    perp_lines.append(perp_line)

# Create a GeoDataFrame for perpendicular lines
perp_gdf = gpd.GeoDataFrame(geometry=perp_lines, crs=sword_nodes_gdf.crs)



## Step 4: Save to shapefile or visualize
output_path = r".../perpendicular_lines_len006_space_sword_nodes.shp"

perp_gdf.to_file(output_path, driver='ESRI Shapefile')   # If it reports an error with NaN or None geometries, run Step 5.



## Step 5: Drop the rows where geometry is None, which will cause error when saving to shapefile

# Check for invalid geometries (NaN or None geometries)
invalid_geometries = perp_gdf[~perp_gdf.is_valid | perp_gdf.is_empty]

# Print the invalid rows
print(invalid_geometries)


# Check for NaN or Infinite Coordinate Values

# Remove geometries with NaN or infinite coordinate values
perp_gdf['geometry'] = perp_gdf['geometry'].apply(lambda geom: geom if geom.is_valid and np.isfinite(geom.length) else None)

# Drop rows where geometry is None
perp_gdf_cleaned = perp_gdf.dropna(subset=['geometry'])

# Save the cleaned GeoDataFrame to a shapefile
output_path = r".../perpendicular_lines_len006_space_sword_nodes_cleaned.shp"
perp_gdf_cleaned.to_file(output_path, driver='ESRI Shapefile')





