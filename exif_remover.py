# Disclaimer: This script is for educational purposes only.
# Do not use against any photos that you don't own or have authorization to test.

#!/usr/bin/env python3

# This script removes EXIF data from images by copying pixel data, but not EXIF data to a new image,
# overriding the original image in your "/images" folder."

# Ensure you run this script from the "/images" folder that contains the image you want to remove EXIF data from.

print(""" _______  _____ _____   ____  _____ __  __  _____     _______ ____  
| ____\ \/ /_ _|  ___| |  _ \| ____|  \/  |/ _ \ \   / / ____|  _ \ 
|  _|  \  / | || |_    | |_) |  _| | |\/| | | | \ \ / /|  _| | |_) |
| |___ /  \ | ||  _|   |  _ <| |___| |  | | |_| |\ V / | |___|  _ < 
|_____/_/\_\___|_|     |_| \_\_____|_|  |_|\___/  \_/  |_____|_| \_\ """)
print("********************************************************************")
print("****    Created by Corbin Parsley (https://github.com/cr0bb)    ****")
print("********************************************************************")

import os
from PIL import Image

cwd = os.getcwd()
if cwd.endswith("/images"):
    print("Images folder detected.")
else:
    print("Images folder not detected. Please run this script from the images folder.")
    exit()

image = input("What image you want to remove EXIF data from?: ")

## Method to check if exif data exists
def has_exif(i):
    try:
        data = i._getexif()
        return bool(data)
    except AttributeError:
        return False

for file in os.listdir(cwd):
    try:
        if file != image:
            continue

        img = Image.open(file)

        if has_exif(img) == False:
            print("No EXIF data found in this image.")
            break

        # Create new image
        image_no_exif = Image.new(img.mode, img.size)

        # Copy pixel data to new image, but not exif data
        img_data = img.getdata()
        image_no_exif.putdata(img_data)

        # Save image
        image_no_exif.save(file)
        print(f"EXIF data removed from {file}")
    except IOError:
        print(f'File format "{file[len(file) - 3]}" not supported')



