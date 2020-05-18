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

INPUT_DIR = './data/edge_frames/'

#  The x, y coordinates of the pixel located in the center of the inlet fitting.
#  these depend on the precise location of the camera
x_center, y_center = 192, 340


# index to number the frames starting from 0
iframe = 0

# pick out only tifs and not hidden files.
# Files are sorted by frame number as long as only one shot of the camera is in the directory.
inext = '.png'
file_list = os.listdir(INPUT_DIR)
file_list = sorted([name for name in file_list if (name.endswith(inext) and not name.startswith('.'))])

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

    # make empty lists to hold the pixel radius data
    radius = []
    angle = []

    for x in range(0, img_array.shape[0]):
        for y in range(0, img_array.shape[1]):
            if img_array[x, y] == 255:
                x_pos = float(x-x_center)
                y_pos = float(y-y_center)
                r = np.sqrt(x_pos**2 + y_pos**2)

                radius.append(r)
                if r != 0.0:   # avoid zero radii, just in case
                    if x_pos != 0.0:  # avoid a divide by zero situation
                        angle.append(np.arctan(y_pos / x_pos))   # in radians
                    else:
                        if y_pos > 0.0:
                            angle.append(np.pi/2.0)
                        else:
                            angle.append(-np.pi/2.0)
                else:  # angle is undefined for zero radius: just make it zero
                    angle = 0.0   # this should never happen

    # end of the loop over 1 frame

    # # uses an interquartile radius test to eliminate outliers due to stray black pixels
    # radius, angle = fvf.kill_outliers(radius, angle)

    fplot = fplot + [iframe]
    rplot = rplot + [np.mean(radius)]
    # standard deviation is a measure of how noncircular the bubble is.
    stdplot = stdplot + [np.std(radius)]

    rmaxplot = rmaxplot + [max(radius)]
    rminplot = rminplot + [min(radius)]

    # Use a quick plot to check for outliers due to wild stray pixels
    # these should have been eliminated by kill_outliers function
    # plt.plot(angle,radius,'.')
    # plt.show()

    # go to the next frame
    iframe += 1

# save the data to a file for further analysis later
OUTPUT_DIR = './data/radius_results/'

np.savetxt(OUTPUT_DIR + '_radius_data.txt', (fplot,rplot,stdplot,rmaxplot,rminplot))

plt.plot(fplot, rplot, label='avg radius')
plt.plot(fplot, stdplot, label='std dev')
plt.plot(fplot, rmaxplot, label=r'$R_{max}$')
plt.plot(fplot, rminplot, label= r'$R_{min}$')
plt.xlabel('frame number')
plt.ylabel('radius (in pixels)')
plt.title('Radii ' + OUTPUT_DIR)
plt.legend(loc='upper left')

plt.savefig(OUTPUT_DIR+'radii.pdf')
plt.show()

plt.close()

plt.plot(fplot, rplot, label='avg radius')
plt.xlabel('frame number')
plt.ylabel('radius (in pixels)')
plt.title('Radii ' + OUTPUT_DIR)
plt.legend(loc='upper left')

plt.savefig(OUTPUT_DIR+'radii_only.pdf')
plt.show()

