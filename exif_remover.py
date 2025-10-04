# Disclaimer: This script is for educational purposes only.
# Do not use against any photos that you don't own or have authorization to test.

#!/usr/bin/env python3

# This program is for .JPG and .TIFF format files.
# Installation and usage instructions:
# 1. Install Pillow (Pillow will not work if you have PIL installed):
# python3 -m pip install --upgrade pip
# python3 -m pip install --upgrade Pillow
# 2. Add .jpg images to subfolder ./images from where the script is stored.
# 3. Run the script: python3 exif_remover.py

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
if not os.path.isdir(os.path.join(cwd, "images")):
	print("Images folder not detected, ensure you have a './images' subfolder")
	exit()
else:
    print("Images folder detected")
    os.chdir(os.path.join(cwd, "images"))
    cwd = os.getcwd()


image = input("What image you want to remove EXIF data from?: ")

if image.strip() not in os.listdir(cwd):
	print("File not found")
	exit()

## Method to check if exif data exists
def has_exif(i):
    try:
        data = i._getexif()
        return bool(data)
    except AttributeError:
        return False

for file in os.listdir(cwd):
    try:
        if file != image.strip():
            continue

        img = Image.open(file)

        if not has_exif(img):
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
        print(f'File format {file[file.index("."):]} not supported')



