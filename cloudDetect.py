# Maddie Schwarz 6/26/23
# QUAKES-I data processing

'''This script detects images containing clouds and saves images WITHOUT clouds to a separate folder.
The script applies a threshold to segment cloud regions in the image. 
It then calculates the percentage of cloud pixels in the image and compares it to a threshold value. 
Adjust the threshold percentage based on your specific requirements. 
'''

import cv2
import os
import shutil

# Specify the folder path containing the images
folder_path = "death-valley-line1_updated/death-valley-line1"       #/path/to/folder"
output_folder_path = "death-valley-line1_updated/DVline1_noClouds" 

# Function to check if an image contains clouds
def contains_clouds(image_path, threshold=200):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to segment cloud regions
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Count the number of white pixels (cloud pixels) in the binary image
    white_pixel_count = cv2.countNonZero(binary)

    # Calculate the total number of pixels in the image
    total_pixels = binary.shape[0] * binary.shape[1]

    # Calculate the percentage of cloud pixels
    cloud_percentage = (white_pixel_count / total_pixels) * 100

    # Set a threshold percentage for cloud presence
    cloud_threshold = 50  # Adjust as per your requirement

    # Return True if the cloud percentage exceeds the threshold
    return cloud_percentage >= cloud_threshold

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        # Generate the file path
        image_path = os.path.join(folder_path, filename)

        # Check if the image contains clouds
        if contains_clouds(image_path):
            print(f"The image {filename} contains clouds.")
        else:
            print(f"The image {filename} does not contain clouds.")
            # Generate the output file path for images without clouds
            output_path = os.path.join(output_folder_path, filename)
            shutil.copy2(image_path, output_path)