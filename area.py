"""
Code for processing fractal viscous fingering images
by extracting radius and angle information from binarized images.

Stephen Morris August 2017

How to use this code for processing binarized FVF (just outlines: not floodfilled) images:

Images are assumed to have been be binarized using
 empty_pipe = True
 edge_pipe = False
in the process_FVF_images.py code.

All binarized images are stored in the image folder named in the code below.  They should
look like just black outlines of the bubble, with a white gap and no inlet pipe etc.

This code finds the mean radius and some statistics versus the frame number.
You must supply the x,y coodinates of the centre of the inlet pipe fitting.
These values should match the ones previously used in the process_FVF_images.py code

You can uncomment a quick plot to check for outliers below.

Results are stored in a text file called image_folder_name_radius_data.txt
for further analysis.  At this stage, the units are still pixels and frame numbers.

"""

import os
import os.path as path

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from tqdm import tqdm


def calculate_area(input_directory, output_directory, input_extension, video_name):
    input_directory = path.join(input_directory, 'bw_frames')
    output_directory = path.join(output_directory, 'area_results')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # index to number the frames starting from 0
    iframe = 0

    file_list = os.listdir(input_directory)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    fplot = []  # frame numbers for plotting
    aplot = []  # radii

    for image_file_name in tqdm(file_list):
        img = Image.open(path.join(input_directory, image_file_name))

        # the transpose makes the coordinates of images match those of matrices
        img_array = np.array(img).transpose()
        img.close()

        # # uses an interquartile radius test to eliminate outliers due to stray black pixels
        # radius, angle = fvf.kill_outliers(radius, angle)

        fplot = fplot + [iframe]
        aplot = aplot + [np.count_nonzero(img_array)]

        # go to the next frame
        iframe += 1

    np.savetxt(output_directory + '/area_data.txt', (fplot, aplot))

    plt.plot(fplot, aplot, label='area')
    plt.xlabel('frame number')
    plt.ylabel('area (in pixels)')
    plt.title('Area ' + video_name)
    plt.legend(loc='upper left')

    plt.savefig(output_directory+'/area.pdf')
    plt.show()

    plt.close()
