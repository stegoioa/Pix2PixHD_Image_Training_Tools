import cv2
import numpy as np
import os
from PIL import Image

# Define the input and output folders
input_folder = r'C:\Users\Anwender\Documents\FLOORPLANPROCESSING\OUTPUT_ROTATED'
output_folder = r'C:\Users\Anwender\Documents\FLOORPLANPROCESSING\OUTPUT_MASK'

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Loop through all the files in the input folder
for root, dirs, files in os.walk(input_folder):
    for file in files:
        # Check if the file is a PNG
        if file.endswith('.png'):
            # load the PNG file using Pillow
            png_path = os.path.join(root, file)
            img = Image.open(png_path)
            # create a new image with a white background and the same size as the original image
            white_img = Image.new('RGBA', img.size, (255, 255, 255, 255))
            # apply the alpha mask of the original image to the white image
            white_img.putalpha(img.split()[-1])

            # Extract the alpha channel
            alpha = np.array(white_img)[:,:,3]

            # Reduce small holes in the alpha channel
            kernel = np.ones((7,7), np.uint8)
            closed_alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel)

            # Perform edge detection on the alpha channel
            edges = cv2.Canny(closed_alpha, 100, 200)

            # Dilate the edges to make them thicker
            kernel = np.ones((15,15), np.uint8)
            dilated_edges = cv2.dilate(edges, kernel)

            # Draw the dilated edges on the original image
            img_array = np.array(white_img)
            img_array[dilated_edges == 255] = (0, 0, 0, 255)
            img = Image.fromarray(img_array)

            # Save the masked image to the output folder with the same filename
            output_path = os.path.join(output_folder, file)
            img.save(output_path)
