import cv2
import numpy as np
import os

# Define the input and output folders
input_folder = r'C:\Users\Anwender\Desktop\testsvg\inputfolder'
output_folder = r'C:\Users\Anwender\Desktop\testsvg\outputfolder'

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Loop through all the files in the input folder
for root, dirs, files in os.walk(input_folder):
    for file in files:
        # Check if the file is a PNG
        if file.endswith('.png'):
            # Load the input image
            img = cv2.imread(os.path.join(root, file), cv2.IMREAD_UNCHANGED)

            # Convert the image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Threshold the grayscale image to create a binary mask
            _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

            # Find contours in the binary mask
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)

            # Create a mask image of the largest white area
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [largest_contour], -1, 255, -1)

            # Create a copy of the original image
            img_copy = img.copy()

            # Convert white pixels in the original image to grey
            img_copy[mask == 255] = cv2.addWeighted(img_copy[mask == 255], 0.8, np.zeros_like(img_copy[mask == 255]), 0.2, 0)

            # Draw the largest white area in red on the copy image
            cv2.drawContours(img_copy, [largest_contour], -1, (0, 0, 255), -1)

            # Add the alpha channel from the original image onto the copy image
            img_copy[:, :, 3] = img[:, :, 3]

            # Save the result to the output folder with the same filename
            output_path = os.path.join(output_folder, file)
            cv2.imwrite(output_path, img_copy)
