# QUAKES-photogrammetry
Scripts for processing QUAKES-I stereo photogrammetry data

#----------------------------------------------------------
# Python Setup Information:
Python 3.10

pip install Pillow 

pip install opencv-python-headless

pip install piexif

pip install laspy[lazrs,laszip]

#----------------------------------------------------------
# Script list
cloudDetect.py -- filter out images that contain clouds (note: sensitive to threshold % parameter)

greyImages.py  -- convert images to greyscale while retaining EXIF GPS metadata

generateRef.py -- create a geotag reference txt file for images using QUAKES camera orientations

getPCextent.py -- load a point cloud .LAZ file and get the lat/long coords of its extent for ref data search on OpenTopography
