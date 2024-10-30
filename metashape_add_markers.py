import Metashape, os
doc = Metashape.app.document
chunk = doc.chunk

# print markers' coordinates
points_dic={}
for point in chunk.markers:
    print(point, point.position)
    points_dic[point.label]=point.position
points_dic={}

for point in chunk.markers:

    print(point, point.position)

    points_dic[point.label]=point.position

