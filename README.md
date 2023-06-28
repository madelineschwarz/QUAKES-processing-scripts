# QUAKES-photogrammetry
Scripts for processing QUAKES-I stereo photogrammetry data

#----------------------------------------------------------
# Python Setup Information:
Python 3.10

pip install Pillow 

pip install opencv-python-headless

pip install piexif

#----------------------------------------------------------
# Script list
cloudDetect.py -- filter out images that contain clouds

greyImages.py  -- convert images to greyscale while retaining EXIF GPS metadata

generateRef.py -- create a geotag reference txt file for images using QUAKES camera orientations
