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


def mean_radius(input_directory, output_directory, input_extension, video_name, tansposed_x_center, tansposed_y_center):
    input_directory = path.join(input_directory, 'edge_frames')
    output_directory = path.join(output_directory, 'radius_results')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # index to number the frames starting from 0
    iframe = 0

    # pick out only tifs and not hidden files.
    # Files are sorted by frame number as long as only one shot of the camera is in the directory.
    file_list = os.listdir(input_directory)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    fplot = []  # frame numbers for plotting
    rplot = []  # radii
    stdplot = []  # std dev
    rmaxplot =[]  # max radius
    rminplot =[]  # min radius

    jump = 100

    for image_file_name in tqdm(file_list[0::jump]):
        img = Image.open(path.join(input_directory, image_file_name))

        # the transpose makes the coordinates of images match those of matrices
        img_array = np.array(img).transpose()

        img.close()

        # make empty lists to hold the pixel radius data
        radius = []

        for x in range(0, img_array.shape[0]):
            for y in range(0, img_array.shape[1]):
                if img_array[x, y] == 255:
                    x_pos = float(x-tansposed_y_center)
                    y_pos = float(y-tansposed_x_center)
                    r = np.sqrt(x_pos**2 + y_pos**2)

                    radius.append(r)


        fplot = fplot + [iframe]
        rplot = rplot + [np.mean(radius)]
        # standard deviation is a measure of how noncircular the bubble is.
        stdplot = stdplot + [np.std(radius)]

        rmaxplot = rmaxplot + [max(radius)]
        rminplot = rminplot + [min(radius)]

        # go to the next frame
        iframe += 1
    np.savetxt(output_directory + '/radius_data.txt', (fplot, rplot, stdplot, rmaxplot, rminplot))

    plt.scatter(fplot, rplot, label='avg radius')
    plt.scatter(fplot, stdplot, label='std dev')
    plt.scatter(fplot, rmaxplot, label=r'$R_{max}$')
    plt.scatter(fplot, rminplot, label= r'$R_{min}$')
    plt.xlabel('frame number')
    plt.ylabel('radius (in pixels) ' + video_name)
    plt.title('Radii ' + video_name)
    plt.legend(loc='upper left')

    plt.savefig(output_directory + '/radii.pdf')
    plt.show()

    plt.close()

    vel = []
    fps = 50.0
    for i in range(len(rplot)-2):
        dr = rplot[i+1] - rplot[i]
        dt = (1.0/fps)*jump
        vel = vel + [dr/dt]

    np.savetxt(output_directory + '/vel_data.txt', vel)

    plt.scatter(list(np.array(range(len(vel))) * (1/fps)*jump), vel, label='vel')
    plt.xlabel('time (sec)')
    plt.ylabel('vel')
    plt.title('vel ' + video_name)
    plt.legend(loc='upper left')

    plt.savefig(output_directory+'/vel.pdf')
    plt.show()

    plt.close()
    #
    # time = list(np.array(range(len(rplot))) * (1/fps))
    # R_fit_coef = np.polyfit(time, rplot, 4)
    # v_fit_coef = np.polyder(R_fit_coef)
    #
    # initial_radius = np.polyval(R_fit_coef, time)[0] #value should be similar to radii[0]
    # initial_velocity = np.polyval(v_fit_coef, time)[1]
    #
    # np.polyval(v_fit_coef, time)
    #
    # plt.plot(time, np.polyval(v_fit_coef, time), label='vel')
    # plt.xlabel('time (sec)')
    # plt.ylabel('vel')
    # plt.title('vel2')
    # plt.legend(loc='upper left')
    #
    # plt.savefig(OUTPUT_DIR+'vel2.pdf')
    # plt.show()
    #
    # plt.close()
    #
