# Functions for handling images for coregistration using CV2 
import os
import imghdr
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
from osgeo import gdal

def check_img_file_type(image_path):
    '''check whether input image is a tiff or jpeg 
    
    '''
     # Load the image using tifffile or cv2
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    # Get image type
    image_type = imghdr.what(image_path)
    # Open Image with Tiffile or CV2
    if image_type == 'tiff' or image_path.lower().endswith('.tif'):
        image = tiff.imread(image_path)
    elif image_type  == 'jpeg'or image_path.lower().endswith(('.jpg', '.jpeg')):
        image = cv2.imread(image_path)
    else:
        raise ValueError("Unsupported image format. Only TIFF and JPG are supported.")
    print('Image path: ', image_path)
    print('Image type: ', image_type)
    print('Image dimensions: ', image.ndim)
    print('Image shape: ', image.shape)
    return image, image_type

def save_img_as_rgb(image_path, output_img_path):
    ''' convert a multi-spectral image (e.g. RGBA) to a three band RGB image
    image_path: path to input image 
    output_img_path: output path for new rgb image
    
    '''
    # Load the image using tifffile or cv2
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    # Get image type
    image, image_type = check_img_file_type(image_path)
    # Fix shape if bands are first (e.g., (4, H, W))
    if image.ndim == 3 and image.shape[0] <= 4:  
        image = np.transpose(image, (1, 2, 0))  # Convert to (H, W, C)
        print('Corrected image shape to CV2 standards: ', image.shape)
    # Ensure image has 3 dimensions
    if image.ndim == 2:
        pass  # Already grayscale
    elif image.ndim == 3:
        if image.shape[2] > 3:
            image = image[:, :, :3]  # Keep only 3 bands
            print('sliced image dimensions: ', image.ndim, 'sliced image shape: ', image.shape)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    else:
        raise ValueError("Error: Unexpected image dimensions.")

    # Normalize and convert to 8-bit
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Save new RGB image
    if image_type == 'tiff' or image_path.lower().endswith('.tif'):
      tiff.imwrite(output_img_path, image)
    elif image_type  == 'jpeg' or image_path.lower().endswith(('.jpg', '.jpeg')):
        cv2.imwrite(output_img_path, image)
    else:
        raise ValueError("Unsupported image format. Only TIFF and JPG are supported. Unable to save image.")
    
    
def load_image(image_path):
    ''' load and prep images for co-registration
    
      '''
    # Load the image using tifffile or cv2
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    # Get image type
    image, image_type = check_img_file_type(image_path)

    # image.ndims should = 3
    # image.shape should be (height, width, channels)
    # some images may be in an alternate shape ex: (channels, height, width)
    # Fix shape if bands are first (e.g., (4, H, W))
    if image.ndim == 3 and image.shape[0] <= 4:  
        image = np.transpose(image, (1, 2, 0))  # Convert to (H, W, C)
        print('Corrected image shape to CV2 standards: ', image.shape)
    # Ensure image has 3 dimensions
    if image.ndim == 2:
        pass  # Already grayscale
    elif image.ndim == 3:
        if image.shape[2] > 3:
            image = image[:, :, :3]  # Keep only 3 bands
            print('sliced image dimensions: ', image.ndim, 'sliced image shape: ', image.shape)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    else:
        raise ValueError("Error: Unexpected image dimensions.")
    # Normalize and convert to 8-bit
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return image

def align_img_corners(non_referenced_img, georeferenced_image):
    '''
    Takes a non-georeferenced image and a georeferenced image and aligns the upper left-hand corner
    of the non-georeferenced image with the corner of the referenced one. Saves the new corner-aligned 
    image.
    
        non_referenced_img: path to input image that lacks any georeferencing
        georeferenced_image: path to second input image that is georeferenced
    '''
    # Open the non-georef image as read only file and get transform and projection (should be None)
    non_dataset = gdal.Open(non_referenced_img, gdal.GA_ReadOnly)
    if non_dataset is None:
        raise FileNotFoundError(f"Could not open file: {non_referenced_img}")
    non_img_geotransform = non_dataset.GetGeoTransform()  # Affine transform
    non_img_projection = non_dataset.GetProjection()  # CRS info
    image_type = imghdr.what(non_referenced_img)

    # Open the georef image as read only file and get transform and projection
    georef_dataset = gdal.Open(georeferenced_image, gdal.GA_ReadOnly)
    if georef_dataset is None:
        raise FileNotFoundError(f"Could not open file: {georeferenced_image}")
    geotransform = georef_dataset.GetGeoTransform()  # Affine transform
    projection = georef_dataset.GetProjection()  # CRS info

    print('Non-ref Image geotransform: ', non_img_geotransform)
    print('Non-ref Image CRS: ', non_img_projection)
    print('ref Image geotransform: ', geotransform)
    print('Image CRS: ', projection)
    # get proper GDAL driver based on image type (Tiff or JPG)
    if image_type == 'tiff' or non_referenced_img.lower().endswith('.tif'):
        driver = driver = gdal.GetDriverByName("GTiff")
        filetype = '.tif'
    elif image_type  == 'jpeg' or non_referenced_img.lower().endswith(('.jpg', '.jpeg')):
        driver = driver = gdal.GetDriverByName("JPEG")
        filetype = '.jpeg'
    else:
        raise ValueError("Unsupported image format. Only TIFF and JPG are supported.")
    
    # Create a copy of the non-georeferenced image to modify 
    base_name, _ = os.path.splitext(non_referenced_img)
    copy_non_ref_img = 'copy'+base_name+filetype
    copy_nondataset = driver.CreateCopy(copy_non_ref_img, non_dataset, 0)
    copy_nondataset.SetGeoTransform(non_img_geotransform)  # Copy geotransform
    copy_nondataset.SetProjection(non_img_projection)  # Copy projection

    # Set geotransform & of copy image to that of georeferenced image
    copy_nondataset.SetGeoTransform(geotransform)
    copy_nondataset.SetProjection(projection)
    
    print(f"New Geotransform for {copy_non_ref_img}: ", copy_nondataset.GetGeoTransform())
    print(f"New Projection for {copy_non_ref_img}: ", copy_nondataset.GetProjection())

    non_dataset = None
    georef_dataset = None
    copy_nondataset = None
    return copy_non_ref_img

