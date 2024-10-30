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
with open(r"elev_markers.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        print ('line[{}] = {}'.format(i, line))

# TODO: Write markers from file (create markers)

