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

# TODO: Read txt or csv file (long, lat, elevation)
# TODO: Write markers from file (create markers)

