"""  Box counting algorithm for estimating fractal dimension of a binarized image.

Adapted from
https://francescoturci.wordpress.com/2016/03/31/box-counting-in-numpy/

Stephen Morris August 2017

"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os.path as path
import os

from tqdm import tqdm


def box_count(pixels, size, start=1, end=3, iterations=20):
    """ Compute the fractal dimension using the box count algorithm

    Parameters
    ----------
    pixels : array
        An Nx2 array of pixel locations
    size : tuple(int, int)
        The size of the image (e.g. `img.size`)
    start : number
        starting power of 2
    end : number
        ending power of 2
    iterations: int
        How many iterations of the algorithm to perform

    Returns
    -------
    array[float]
        The sizes of the box tiling
    list[int]
        The number of boxes with pixels at each scale in the sequence
    """
    scales = np.logspace(2 ** start, 2 ** end, num=iterations, endpoint=False, base=2)
    Ns = []
    Lx, Ly = size
    for scale in scales:
        # We use histogramdd to count the pixels in each region (box)
        bins = (np.arange(0, Lx, scale), np.arange(0, Ly, scale))
        H, _ = np.histogramdd(pixels, bins=bins)
        # The number of non-empty boxes is counted by fist making H binary (1 or 0)
        Ns.append(np.sum(H > 0))
    return scales, Ns


def bow_count_last_frame():
    video_names = ['video3_001', 'video5_003', 'video6_001', 'video7_001', 'video8_001', 'video9_001', 'video10_001', 'video11_001']
    video_frame = ['004501', '000757', '000539', '000528', '000603', '001503', '000362', '000584']

    for i in range(len(video_names)):
        video_name = video_names[i]
        print('\n####### Working on: ' + video_name + ' #######')
        image_file_name = '/Users/rotemmayo/Documents/AdvLabFVF/176lab/' + video_name + '_results/bw_frames/frame' + video_frame[i] + '.jpg'

        image = Image.open(image_file_name)
        p = np.argwhere(image)
        scales, Ns = box_count(p, image.size)

        # Perform a linear fit (a polynomial of degree 1 is a line)
        coeffs = np.polyfit(np.log(scales), np.log(Ns), 1)
        dimension = -coeffs[0]

        plt.plot(np.log(scales), np.log(Ns), 'o', mfc='none', label='data')
        plt.plot(np.log(scales), np.polyval(coeffs, np.log(scales)), label='fit')
        plt.xlabel('log $\epsilon$')
        plt.ylabel('log N')
        plt.title('{} D = {}'.format(image_file_name, dimension))
        plt.legend()
        plt.savefig('/Users/rotemmayo/Documents/AdvLabFVF/176lab/' + video_name + '_results/' + '_powerlaw.pdf')

        print('The Hausdorff dimension is ', dimension)


def box_count_all_frames(input_directory, output_directory, input_extension, video_name, start_frame, end_frame):
    input_directory = path.join(input_directory, 'bw_frames')
    output_directory = path.join(output_directory, 'box_count_results')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # index to number the frames starting from 0
    iframe = 0

    file_list = os.listdir(input_directory)
    file_list = sorted(
        [name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    fplot = []  # frame numbers for plotting
    hdplot = []  # radii

    for image_file_name in tqdm(file_list):
        img = Image.open(path.join(input_directory, image_file_name))
        p = np.argwhere(img)
        scales, Ns = box_count(p, img.size)
        img.close()

        # Perform a linear fit (a polynomial of degree 1 is a line)
        coeffs = np.polyfit(np.log(scales), np.log(Ns), 1)
        dimension = -coeffs[0]

        # # uses an interquartile radius test to eliminate outliers due to stray black pixels
        # radius, angle = fvf.kill_outliers(radius, angle)

        fplot = fplot + [iframe]
        hdplot = hdplot + [dimension]

        # go to the next frame
        iframe += 1

    np.savetxt(output_directory + '/hd_data.txt', (fplot, hdplot))

    plt.plot(fplot, hdplot, label='h dimension')
    plt.xlabel('frame number')
    plt.ylabel('Hausdorff dimension')
    plt.title('Hausdorff dimension ' + video_name)
    plt.legend(loc='upper left')

    plt.savefig(output_directory + '/h_dimension.pdf')
    plt.show()

    plt.close()


video_names = ['video3_001', 'video5_003', 'video6_001', 'video7_001', 'video8_001', 'video9_001', 'video10_001', 'video11_001']
video_start = [2720,            237,        163,            256,        328,            1319,       242,            472]
video_end =   [4501,            757,        539,            528,        603,            1503,       362,            584]

for i in range(len(video_names)):
    video_name = video_names[i]
    print('\n####### Working on: ' + video_name + ' #######')
    input_directory = '/Users/rotemmayo/Documents/AdvLabFVF/176lab/' + video_name + '_results'

    box_count_all_frames(input_directory, input_directory, 'jpg', video_name, video_start[i], video_end[i])

