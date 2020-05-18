import shutil

import numpy as np
import matplotlib.pyplot as plt

from skimage import measure
import os
import os.path as path

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from tqdm import tqdm

INPUT_DIR = './data/edge_frames/'
OUTPUT_DIR = './data/contoure_frames/'

shutil.rmtree(OUTPUT_DIR)
os.mkdir(OUTPUT_DIR)

# index to number the frames starting from 0
start_frame_index = 124
end_frame_index = 134


# pick out only tifs and not hidden files.
# Files are sorted by frame number as long as only one shot of the camera is in the directory.
input_extension = '.png'
file_list = os.listdir(INPUT_DIR)
file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])
# file_list = file_list[start_frame_index:end_frame_index]
fplot = []  # frame numbers for plotting
rplot = []  # radii
stdplot = []  # std dev
rmaxplot =[]  # max radius
rminplot =[]  # min radius


for image_file_name in tqdm(file_list):
    img = Image.open(path.join(INPUT_DIR, image_file_name))

    # the transpose makes the coordinates of images match those of matrices
    img_array = np.array(img).transpose()

    img.close()

    # Find contours at a constant value of 0.8
    contours = measure.find_contours(img_array, 0.8, fully_connected='high')

    # Display the image and plot all contours found
    fig, ax = plt.subplots()
    ax.imshow(img_array, cmap=plt.cm.gray)

    for n, contour in enumerate(contours):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    image_file_name = image_file_name.replace(input_extension, '')
    plt.savefig(OUTPUT_DIR + image_file_name + '.pdf')
    # plt.show()
    plt.close()
    # np.savetxt(OUTPUT_DIR + image_file_name + '.txt', [[contour[:, 1], contour[:, 0]] for contour in contours], fmt='%s')


