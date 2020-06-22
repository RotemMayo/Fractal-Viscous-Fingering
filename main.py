from process_video import convert_to_bw, find_edge, make_movie, add_number
from area import calculate_area
from perimiter import calculate_perimiter
import os

video_names = ['video3_001', 'video5_003', 'video6_001', 'video7_001', 'video8_001', 'video9_001', 'video10_001', 'video11_001']
# video_names = ['video2_001']

for video_name in video_names:
    print('\n####### Working on: ' + video_name + ' #######')
    input_directory = '/Users/rotemmayo/Documents/AdvLabFVF/176lab/' + video_name
    output_directory = '/Users/rotemmayo/Documents/AdvLabFVF/176lab/' + video_name + '_results'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    input_extension = '.jpg'
    file_list = os.listdir(input_directory)
    file_list = sorted([name for name in file_list if (name.endswith(input_extension) and not name.startswith('.'))])
    start_number = int(file_list[0].rsplit('e')[1].rsplit('.')[0])

    #  The TRANSPOSED x, y coordinates of the pixel located in the center
    tansposed_x_center, tansposed_y_center = 341, 384

    R_MIN = 70.
    R_MAX = 300.

    print('### Convert to BW ###')
    convert_to_bw(input_directory, output_directory, input_extension, tansposed_x_center, tansposed_y_center, R_MIN, R_MAX)
    print('### Find Edge ###')
    find_edge(output_directory, output_directory, input_extension, tansposed_x_center, tansposed_y_center, R_MIN, R_MAX)
    print('### Add Number Edge ###')
    add_number(output_directory, output_directory, input_extension, 'edge_frames')
    print('### Make Movie edge ###')
    make_movie(start_number, output_directory, output_directory, 'edge_frames', video_name)
    print('### Add Number BW ###')
    add_number(output_directory, output_directory, input_extension, 'bw_frames')
    print('### Make Movie BW ###')
    make_movie(start_number, output_directory, output_directory, 'bw_frames', video_name)
    print('### Calculate Area ###')
    calculate_area(output_directory, output_directory, input_extension, video_name)
    print('### Calculate Perimiter ###')
    calculate_perimiter(output_directory, output_directory, input_extension, video_name)

