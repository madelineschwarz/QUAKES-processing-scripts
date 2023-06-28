from PIL import Image
import piexif
import os

# Specify the folder path containing the images
folder_path = "death-valley-line1_updated/death-valley-line1" #"/path/to/folder"
# Specify the output folder path
output_folder_path = "GREY_line1_updated" #"/path/to/output/folder"

# Function to convert image to grayscale while preserving metadata
def convert_to_grayscale(image_path, output_path):
    image = Image.open(image_path)

    # Check if the image has EXIF metadata
    if "exif" in image.info:
        exif_data = image.info["exif"]

        # Create a new image in grayscale
        image_gray = image.convert("L")

        # Preserve the GPS metadata
        exif_dict = piexif.load(exif_data)
        if "GPS" in exif_dict:
            gps_info = exif_dict["GPS"]
            image_gray_exif = image_gray.copy()
            image_gray_exif.save(output_path, exif=piexif.dump({"GPS": gps_info}))
        else:
            # Save the grayscale image without GPS metadata
            image_gray.save(output_path)
    else:
        # If there is no EXIF metadata, save the grayscale image without it
        image_gray = image.convert("L")
        image_gray.save(output_path)
        
# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        # Generate the input and output file paths
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder_path, filename)
        print(input_path)
        # Convert the image to grayscale
        convert_to_grayscale(input_path, output_path)
    