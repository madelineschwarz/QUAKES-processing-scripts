# Automatically 'pin' markers to images in Agisoft Metashape
# source: https://www.agisoft.com/forum/index.php?topic=13543.0
# Note: only use if default marker positioning is correct 
import Metashape
chunk = Metashape.app.document.chunk
for marker in chunk.markers:
    if marker.type != Metashape.Marker.Type.Regular:
        continue
    for camera in marker.projections.keys():
        marker.projections[camera].pinned = True
