import os
import os.path as path
import warnings

import skimage.io as io
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from tqdm import tqdm

from PIL import ImageDraw


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


def convert_to_bw(input_directory, output_directory, input_extension):
    """
    Read from input directory all images ending with input extension,
    load as greyscale, binarize and save to output_directory under bw_frames
    :param input_directory:
    :param output_directory:
    :param input_extension:
    :return:
    """
    output_directory = path.join(output_directory, 'bw_frames')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    contrast = 1.0  # makes the grey scale gradient steeper to better define the edge of the bubble, 1.0 => no change
    sharpness = 1.0  # emphasizes sharp edges of the bubble, 1.0 => no change
    brightness = 1.5  # lifts the white level to whiter, 1.0 => no change
    bw_threshold = 150  # A number between 0 (black) - 255 (white).

    file_list = os.listdir(input_directory)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    output_extension = '.jpg'

    for image_file_name in tqdm(file_list):
        img = _load_as_greyscale(path.join(input_directory, image_file_name), contrast, sharpness, brightness)
        img = _binarize(img, bw_threshold) * 255

        image_file_name = image_file_name.replace(input_extension, '')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            io.imsave(path.join(output_directory, image_file_name + output_extension), img)


def find_edge(input_directory, output_directory, input_extension, x_center, y_center, r_min, r_max):
    """
    Read from bw_frames, find edge, put on radial mask, save to edge frames

    :param input_directory:
    :param output_directory:
    :param input_extension:
    :param x_center:
    :param y_center:
    :param r_min:
    :param r_max:
    :return:
    """
    input_directory = path.join(input_directory, 'bw_frames')
    output_directory = path.join(output_directory, 'edge_frames')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    file_list = os.listdir(input_directory)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    output_extension = '.jpg'

    for image_file_name in tqdm(file_list):
        img = Image.open(path.join(input_directory, image_file_name))
        img = img.filter(ImageFilter.FIND_EDGES)
        img = _binarize(img, 200) * 255

        img_array = np.array(img).transpose()
        img_array = _radial_mask(img_array, x_center, y_center, r_min, r_max)

        image_file_name = image_file_name.replace(input_extension, '')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            io.imsave(path.join(output_directory, image_file_name + output_extension), img_array)


def add_number(input_directory, output_directory, input_extension, input_type):
    input_directory = path.join(input_directory, input_type)
    output_directory = path.join(output_directory, input_type + '_numbered')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    file_list = os.listdir(input_directory)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])

    for image_file_name in tqdm(file_list):
        img = Image.open(path.join(input_directory, image_file_name))
        number = image_file_name.rsplit('e')[1].rsplit('.')[0]
        draw = ImageDraw.Draw(img)
        draw.text((700, 700), number, fill=255)
        img.save(path.join(output_directory, image_file_name))


def make_movie(start_number, input_directory, output_directory, input_type, video_name):
    input_directory = path.join(input_directory, input_type + '_numbered')
    output_directory = path.join(output_directory, input_type + '_output_video')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    command = "ffmpeg -f image2 -r 20 -start_number " + str(start_number) + " -i " + input_directory + "/frame%06d.jpg -vcodec mpeg4 -y " + output_directory + "/" + video_name + ".mp4"
    os.system(command)

# os.system("ffmpeg -f image2 -r 20 -pattern_type glob -i " + INPUT_DIR + "*.jpg -vcodec mpeg4 -y "+OUTPUT_DIR+"edge_video.mp4")

# def frames_from_movie(video_name):
#     INPUT_DIR = './data/input_video/'
#     OUTPUT_DIR = './data/input_video_frames/'
#
#     shutil.rmtree(OUTPUT_DIR)
#     os.mkdir(OUTPUT_DIR)
#     os.system('ffmpeg -i ' + INPUT_DIR + video_name + '.mp4 ' + OUTPUT_DIR + 'output-%07d.png')
