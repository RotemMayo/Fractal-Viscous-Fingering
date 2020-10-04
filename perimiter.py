

import os
import os.path as path

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from tqdm import tqdm


def calculate_perimiter(input_directory, output_directory, input_extension, video_name):
    input_directory = path.join(input_directory, 'edge_frames')
    output_directory = path.join(output_directory, 'preimiter_results')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # index to number the frames starting from 0
    iframe = 0

    # pick out only tifs and not hidden files.
    # Files are sorted by frame number as long as only one shot of the camera is in the directory.
    file_list = os.listdir(input_directory)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    fplot = []  # frame numbers for plotting
    pplot = []  # radii

    for image_file_name in tqdm(file_list):
        img = Image.open(path.join(input_directory, image_file_name))

        # the transpose makes the coordinates of images match those of matrices
        img_array = np.array(img).transpose()
        img.close()

        # # uses an interquartile radius test to eliminate outliers due to stray black pixels
        # radius, angle = fvf.kill_outliers(radius, angle)

        fplot = fplot + [iframe]
        pplot = pplot + [np.count_nonzero(img_array)]

        # go to the next frame
        iframe += 1

    np.savetxt(output_directory + '/perimiter_data.txt', (fplot, pplot))

    plt.plot(fplot, pplot, label='perimiter')
    plt.xlabel('frame number')
    plt.ylabel('perimiter (in pixels)')
    plt.title('perimiter ' + video_name)
    plt.legend(loc='upper left')

    plt.savefig(output_directory+'/perimiter.pdf')
    plt.show()

    plt.close()
