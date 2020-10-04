

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
