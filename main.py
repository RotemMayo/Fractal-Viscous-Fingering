from process_video import convert_to_bw, find_edge, make_movie, add_number
from area import calculate_area
from perimiter import calculate_perimiter
from mean_radius import mean_radius
import os

video_names = ['video1', 'video2', 'video3', 'video4', 'video5', 'video6', 'video7', 'video8', 'video9', 'video10']
# video_names = ['video8']
for video_name in video_names:
    print('\n####### Working on: ' + video_name + ' #######')
    input_directory = '/Users/rotemmayo/Documents/AdvLabFVF/246lab/' + video_name + '/' + video_name
    output_directory = '/Users/rotemmayo/Documents/AdvLabFVF/246lab/' + video_name + '_results'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    input_extension = '.jpg'
    file_list = os.listdir(input_directory)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])
    # start_number = int(file_list[0].rsplit('e')[1].rsplit('.')[0])

    # NXA4-S3 Camera000000
    start_number = int(file_list[0].rsplit('a')[2].rsplit('.')[0])

    #  The TRANSPOSED x, y coordinates of the pixel located in the center
    tansposed_x_center, tansposed_y_center = 520, 504

    R_MIN = 90.
    R_MAX = 360.

    print('### Convert to BW ###')
    convert_to_bw(input_directory, output_directory, input_extension, tansposed_x_center, tansposed_y_center, R_MIN, R_MAX)
    # print('### Find Edge ###')
    # find_edge(output_directory, output_directory, input_extension, tansposed_x_center, tansposed_y_center, R_MIN, R_MAX)
    # print('### Add Number Edge ###')
    # add_number(output_directory, output_directory, input_extension, 'edge_frames')
    # print('### Make Movie edge ###')
    # make_movie(start_number, output_directory, output_directory, 'edge_frames', video_name)

    print('### Add Number BW ###')
    add_number(output_directory, output_directory, input_extension, 'bw_frames')
    print('### Make Movie BW ###')
    make_movie(start_number, output_directory, output_directory, 'bw_frames', video_name)

    # print('### Calculate Area ###')
    # calculate_area(output_directory, output_directory, input_extension, video_name)
    # print('### Calculate Perimiter ###')
    # calculate_perimiter(output_directory, output_directory, input_extension, video_name)
    # print('### Mean Radius ###')
    # mean_radius(output_directory, output_directory, input_extension, video_name, tansposed_x_center, tansposed_y_center)

