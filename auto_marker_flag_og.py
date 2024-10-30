# Run in Agisoft Metashape Python Console
# Source: https://www.agisoft.com/forum/index.php?topic=12571.0

import Metashape as MS

# set the coordinate ref system of the markers
crs_ = MS.CoordinateSystem("EPSG::%d" % crs)
chunk.marker_crs = crs_

# set the z-accuracy very high because we don't have a good measure for this
chunk.marker_location_accuracy = [0.05, 0.05, 1000]

file = open('./export.csv', "rt")#input file

# skips header
lines = file.readlines()[1:]

for line in lines:
    line = line.strip('\n')
    sp_line = line.rsplit(separation, 6) #splitting line
    # Strip extra quotation marks if they exist
    for i, item in enumerate(sp_line):
        sp_line[i] = item.strip('"')
       
    camera_name = sp_line[0]
    marker_name = sp_line[1]
    x = float(sp_line[2]) #x-coord in pixels
    y = float(sp_line[3]) #y-coord in pixels
    cx = float(sp_line[4]) #world x-coord of marker
    cy = float(sp_line[5]) #world y-coord of marker
    cz = float(sp_line[6]) #world z-coord of marker

    # flag to indicate if marker is found
    flag = 0
   
    # Create a Projection from the pixel coordinates
    pixel_coord = MS.Marker.Projection(MS.Vector([x, y]), True)
   
    # get the camera with same name as the name in current line
    for cam in chunk.cameras:
        if cam.label == camera_name:
           
            #searching for a marker with the same ID as in txt file
            for marker in chunk.markers:
                if marker.label == marker_name:
                    # assign the marker's x,y coords in the current cam
                    marker.projections[cam] = pixel_coord
                    flag = 1
                    break
           
            # if marker ID not yet existing in the chunk then create
            if flag == 0:
                marker = chunk.addMarker()
                marker.label = marker_name

                # assign the marker's x,y coords in the current cam
                marker.projections[cam] = pixel_coord
                # Add the world coordinates to the marker
                marker.Reference.location = MS.Vector([cx, cy, cz])
                # Set the accuracy of the marker's coords
                marker.Reference.accuracy = MS.Vector(accuracy)
                # enable the marker
                marker.Reference.enabled = True

            # move onto the next line of the text file
            break

file.close()
print("Import finished.")
