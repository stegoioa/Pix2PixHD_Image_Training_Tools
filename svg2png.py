import os
import subprocess

# define the paths
source_folder = r'C:\Users\Anwender\Downloads\cubicasa5k\cubicasa5k\high_quality_architectural'
export_folder = r'C:\Users\Anwender\Documents\FLOORPLANPROCESSING\OUTPUT'

# create the export folder if it does not exist
if not os.path.exists(export_folder):
    os.mkdir(export_folder)

# initialize the counter for PNG file names
counter = 1

# loop through all the files in the source folder
for root, dirs, files in os.walk(source_folder):
    for file in files:
        # check if the file is an SVG
        if file.endswith('.svg'):
            # convert the SVG file to PNG using Inkscape
            svg_path = os.path.join(root, file)
            png_path = os.path.join(export_folder, os.path.splitext(file)[0] + f'_{counter}.png')
            subprocess.call(['inkscape', svg_path, '--export-png=' + png_path])

            # increment the counter
            counter += 1
