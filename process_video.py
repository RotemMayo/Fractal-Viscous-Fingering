import os
import os.path as path
import shutil
import warnings

import skimage.io as io
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from tqdm import tqdm


def _load_as_greyscale(filename, contrast_factor=1.0, sharpness_factor=1.0, brightness_factor=1.0):
    """
    :return greyscale (0-255)  numpy array
    """
    img = Image.open(filename)

    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(contrast_factor)

    sharpness = ImageEnhance.Sharpness(img)
    img = sharpness.enhance(sharpness_factor)

    brightness = ImageEnhance.Brightness(img)
    img = brightness.enhance(brightness_factor)

    img_greyscale = img.convert('L')

    # the transpose makes the coordinates of images match those of matrices
    img_array = np.array(img_greyscale).transpose()
    img.close()
    img_greyscale.close()
    return img_array


def _binarize(image, threshold=128):
    """
    :param image: 2D array
    :param threshold: int
    :return: array[bool]
    """
    np_img = np.array(image)
    binary_img = np_img > threshold
    return binary_img


def _radial_mask(img, x_center, y_center, inner, outer):
    w, h = img.shape
    x, y = np.mgrid[:w, :h]
    radius = (x - x_center) ** 2 + (y - y_center) ** 2
    return np.where((radius < inner ** 2) | (radius > outer ** 2), 0, img)


def convert_to_bw():
    INPUT_DIR = './data/input_video_frames'
    OUTPUT_DIR = './data/bw_frames'

    shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)

    CONTRAST = 1.0  # makes the grey scale gradient steeper to better define the edge of the bubble, 1.0 => no change
    SHARPNESS = 1.0  # emphasizes sharp edges of the bubble, 1.0 => no change
    BRIGHTNESS = 1.0  # lifts the white level to whiter, 1.0 => no change

    BW_THRESHOLD = 100  # A number between 0 (black) - 255 (white).

    input_extension = '.png'
    file_list = os.listdir(INPUT_DIR)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    output_extension = '.png'

    for image_file_name in tqdm(file_list):
        img = _load_as_greyscale(path.join(INPUT_DIR, image_file_name), CONTRAST, SHARPNESS, BRIGHTNESS)
        img = _binarize(img, BW_THRESHOLD) * 255

        image_file_name = image_file_name.replace(input_extension, '')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            io.imsave(path.join(OUTPUT_DIR, image_file_name + output_extension), img, check_contrast=False)


def find_edge():
    INPUT_DIR = './data/bw_frames'
    OUTPUT_DIR = './data/edge_frames'

    shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)

    #  The TRANSPOSED x, y coordinates of the pixel located in the center
    x_center, y_center = 340, 192

    R_MIN = 0.
    R_MAX = 140.

    input_extension = '.png'
    file_list = os.listdir(INPUT_DIR)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    output_extension = '.png'

    for image_file_name in tqdm(file_list):
        img = Image.open(path.join(INPUT_DIR, image_file_name))
        img = img.filter(ImageFilter.FIND_EDGES)

        img_array = np.array(img).transpose()
        img_array = _radial_mask(img_array, x_center, y_center, R_MIN, R_MAX)

        image_file_name = image_file_name.replace(input_extension, '')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            io.imsave(path.join(OUTPUT_DIR, image_file_name + output_extension), img_array, check_contrast=False)


def make_movie():
    INPUT_DIR = './data/edge_frames/'
    OUTPUT_DIR = './data/output_video/'

    shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    os.system("ffmpeg -f image2 -r 20 -i " + INPUT_DIR + "output-%07d.png -vcodec mpeg4 -y "+OUTPUT_DIR+"edge_video.mp4")


def frames_from_movie(video_name):
    INPUT_DIR = './data/input_video/'
    OUTPUT_DIR = './data/input_video_frames/'

    shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    os.system('ffmpeg -i ' + INPUT_DIR + video_name + '.mp4 ' + OUTPUT_DIR + 'output-%07d.png')
