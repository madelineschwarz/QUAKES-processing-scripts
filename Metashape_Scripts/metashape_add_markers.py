# Run in Agisoft Metashape (v. 2.1.3) Python Console
import Metashape, os
doc = Metashape.app.document
chunk = doc.chunk

# print markers' coordinates (Read existing markers)
points_dic={}
for point in chunk.markers:
    print(point, point.position)
    points_dic[point.label]=point.position
points_dic={}

for point in chunk.markers:
    print(point, point.position)
    points_dic[point.label]=point.position
    
'''
# TODO: Read txt or csv file (long, lat, elevation)
with open(r"elev_markers.csv", "r") as csv_file:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        print ('line[{}] = {}'.format(i, line))
'''

# TODO: Write markers from file (create markers)
# script source: https://www.agisoft.com/forum/index.php?topic=12571.0
import Metashape as MS
# set the coordinate ref system of the markers
crs_ = chunk.crs #MS.CoordinateSystem("EPSG::%d" % crs)
chunk.marker_crs = crs_
# set the z-accuracy very high because we don't have a good measure for this
chunk.marker_location_accuracy = [0.05, 0.05, 1000]
file = open(r"C:\Users\maddie\Downloads\elev_markers.csv", "rt")#input file
# skips header
lines = file.readlines()[1:]
for line in lines:
    line = line.strip('\n')
    sp_line = line.rsplit(',', -1) #splitting line
    # Strip extra quotation marks if they exist
    for i, item in enumerate(sp_line):
        sp_line[i] = item.strip('"')
               
    #camera_name = sp_line[0]
    marker_name = sp_line[0] #sp_line[1]
    #x = float(sp_line[2]) #x-coord in pixels
    #y = float(sp_line[3]) #y-coord in pixels
    cx = float(sp_line[1]) #float(sp_line[4]) #world x-coord of marker
    cy = float(sp_line[2]) #float(sp_line[5]) #world y-coord of marker
    cz = float(sp_line[3]) #float(sp_line[6]) #world z-coord of marker
    print(cx,cy,cz)

    # flag to indicate if marker is found
    flag = 0
           
    # Create a Projection from the pixel coordinates
    pixel_coord = MS.Marker.Projection(MS.Vector([x, y]), True)
    
    # if marker ID not yet existing in the chunk then create
    if flag == 0:
        marker = chunk.addMarker()
        marker.label = marker_name
        # assign the marker's x,y coords in the current cam
        #marker.projections[cam] = pixel_coord
        # Add the world coordinates to the marker
        marker.Reference.location = MS.Vector([cx, cy, cz])
        # Set the accuracy of the marker's coords
        accuracy = float(10)
        marker.Reference.accuracy = MS.Vector(accuracy)
        # enable the marker
        marker.Reference.enabled = True

        # move onto the next line of the text file
        break

file.close()
print("Import finished.")
