## Maddie Schwarz 6/27/23
## QUAKES-I Stereophotogrammetry Data Processing

''' This script generates a  geotag-reference text file for import into Metashape Agisoft (and Pix4D?).
The script reads images from a specified folder and extracts the GPS coordinates of the camera from the EXIF metadata.
The script then assigns yaw, pitch, roll angles for the camera associated with the picture (specified in the filename).

This information is written to a .txt file in the following format:
image_filename.jpg latitude longitude altitude yaw pitch roll '''

from PIL import Image
import piexif
import os

# Specify the folder path containing the images
folder_path = "GREY_line1_updated" #"/path/to/images/folder"

# Output reference txt file path
output_file_path = "GREY_line1_updated/reference.txt"

#specify hemisphere of Data for latitude and longitude
    # options are N or S (lat) -- E or W (long)
lat_hemisphere = 'N'
long_hemisphere = 'W'


# USER DOES NEED TO MODIFY BELOW THIS LINE #
# --------------------------------------------------------------------------------------------------------------------
# Dictionary mapping QUAKES Camera numbers in the filename to yaw, pitch, and roll values
# Calculated based on the rotation matrix for the QUAKES rig using: https://www.andre-gaschler.com/rotationconverter/
yaw_pitch_roll_mapping = {
    "330070": (-0.0346076, 0.3562238,  0.204373),       # Camera 1 
    "330075": (-0.0294507, 0.1463118, 0.1993807),       # Camera 2 
    "330074": (-0.0287554, -0.1492301, 0.1901376),      # Camera 3 
    "330068": (-0.03647, -0.346837, 0.1805305),         # Camera 4 
    "330076": (0.108897, 0.3525194,  -0.2330414),       # Camera 5 
    "330071": (0.0294507, 0.1463118, -0.1993807),       # Camera 6
    "330077": (-0.0933952, -0.139903, -0.2076473),      # Camera 7
    "330069": (-0.1758361, -0.3329031, -0.2537011)      # Camera 8
}


# Open the reference txt file in write mode
with open(output_file_path, "w") as file:
    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            # Generate the input file path
            input_path = os.path.join(folder_path, filename)

            # Read the image and extract the GPS information
            image = Image.open(input_path)
            exif_data = piexif.load(image.info.get("exif"))
            
            # Extract latitude, longitude, and altitude from GPS information
            if "GPS" in exif_data:
                gps_info = exif_data["GPS"]

                latitude = gps_info.get(piexif.GPSIFD.GPSLatitude)
                longitude = gps_info.get(piexif.GPSIFD.GPSLongitude)

                altitude = gps_info.get(piexif.GPSIFD.GPSAltitude, None)
                #print(filename)
                #print(latitude)
                #print(longitude)
                #print(altitude)
               

                # Convert latitude, longitude, and altitude to decimal degrees format
                latitude_decimal = latitude[0][0] + latitude[1][0] / 60 + (latitude[2][0]/latitude[2][1]) / 3600
                longitude_decimal = longitude[0][0] + longitude[1][0] / 60 + (longitude[2][0]/longitude[2][1]) / 3600
            
            ## Assign negative sign based on Hemisphere
            ## https://geoinfo.sdsu.edu/hightech/LM3/dd1.php#:~:text=In%20Decimal%20Degrees%20format%2C%20the,earth%20the%20coordinate%20is%20located.

                if lat_hemisphere == 'S':
                    latitude_decimal = latitude_decimal * -1
                if long_hemisphere == 'W':
                    longitude_decimal = longitude_decimal * -1
                
                latitude_str = str(latitude_decimal)
                longitude_str = str(longitude_decimal)

                altitude_str = str(altitude[0] / altitude[1]) if altitude else "N/A"
            else:
                latitude_str = "N/A"
                longitude_str = "N/A"
                altitude_str = "N/A"

            # Get the yaw, pitch, and roll values based on the filename
            yaw, pitch, roll = None, None, None
            for key in yaw_pitch_roll_mapping.keys():
                if key in filename:
                    yaw, pitch, roll = yaw_pitch_roll_mapping[key]
                    break

            # Write the image filename, GPS information, and yaw, pitch, roll values to the reference txt file
            #file.write(f"Filename Latitude Longitude Altitude Yaw Pitch Roll\n")
            file.write(f"{filename} {latitude_str} {longitude_str} {altitude_str} {yaw} {pitch} {roll}\n")
            file.write("\n")
