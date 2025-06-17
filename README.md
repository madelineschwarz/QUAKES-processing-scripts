# QUAKES-processing-scripts
This repository contains Python, Metashape, and GoogleEarthEngine scripts for processing QUAKES-I stereo-imaging data into DSMs, DTMs, and orthorectified image mosaics. 

# Table of Contents
 - GEE_scripts
   - QUAKES_GCP_Elevation_sampler -- allows user to determine whether the elevation value sampled from Google Earth samples 1m 3DEP, 10m 3DEP, or 30m SRTM elevation datasets
   - Sample_3DEP_markers.ipynb -- load a shapefile of GCPs (exported from Agisoft Metashape) and sample available 3DEP datasets for elevation values 

- Metashape_Scripts
  - auto_marker_flag_og.py -- automatically flag markers in Metashape ('sets flag to Green')
  - auto_marker_pin.py -- automatically pin markers in Metashape
  - metashape_add_markers.py 
 
- Py_Preprocessing
  - cloudDetect.py -- uses OpenCV2 to filter out images that contain clouds (note: sensitive to threshold % parameter)
  - generateRef.py -- create a geotag reference txt file for images using QUAKES camera pose information from estimated Camera Model
  - getPCextent.py -- load a point cloud .LAZ file and get the lat/long coords of its extent for ref data search on OpenTopography
  - greyImages.py -- convert images to greyscale while retaining EXIF GPS metadata
 
coreg_image_utils.py -- functions for handling images for co-registration with CV2
