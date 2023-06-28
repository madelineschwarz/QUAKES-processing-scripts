# Maddie Schwarz 6/28/23
# QUAKES-I data processing
# Get Geographic Extent of Pointcloud

''' Reads a point cloud .LAZ file and prints the latitude/longitude coordinates
of its extent. Use these to find comparison datasets in OpenTopography'''

import numpy as np
import laspy

# Specify the path to the .LAZ file
file_path = "denseCloud.laz" #"/path/to/point_cloud.laz"

# Open the .LAZ file for reading
point_cloud = laspy.read(file_path)

# Access the header of the LasData object
header = point_cloud.header
print(header)
# Retrieve the geographic extent from the header
min_x, max_x = header.min[0], header.max[0]
min_y, max_y = header.min[1], header.max[1]
min_z, max_z = header.min[2], header.max[2]

# Print the geographic extent
print("Geographic Extent of Point Cloud:")
print("Lower Lon:", min_x, "Lower Lat:", min_y)
print("Upper Lon", max_x, "Upper Lat", min_y)
