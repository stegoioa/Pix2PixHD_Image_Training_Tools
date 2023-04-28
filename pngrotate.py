import os
import random
from PIL import Image

# define the path to the folder containing the PNG files
png_folder = r'C:\Users\Anwender\Documents\FLOORPLANPROCESSING\OUTPUT_UNROTATED'
output_folder = r'C:\Users\Anwender\Documents\FLOORPLANPROCESSING\OUTPUT_ROTATED'

# create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# loop through all the files in the folder
for root, dirs, files in os.walk(png_folder):
    for file in files:
        # check if the file is a PNG
        if file.endswith('.png'):
            # load the PNG file using Pillow
            png_path = os.path.join(root, file)
            img = Image.open(png_path)
            # rotate the contents of the PNG file randomly around the center of the canvas
            img = img.rotate(random.uniform(0, 360), center=(img.width/2, img.height/2), expand=True)
            # get the rotated image bounds
            img_bounds = img.getbbox()
            if img_bounds is None:
                # skip this image if it has no content
                continue
            # calculate the size of the new canvas
            new_size = (img_bounds[2] - img_bounds[0], img_bounds[3] - img_bounds[1])
            # create a new canvas with the new size and paste the rotated image onto it
            new_img = Image.new('RGBA', new_size, (0, 0, 0, 0))
            new_img.paste(img, (-img_bounds[0], -img_bounds[1]))
            # save the rotated and rescaled image to the output folder with the same filename
            output_path = os.path.join(output_folder, file)
            new_img.save(output_path)
