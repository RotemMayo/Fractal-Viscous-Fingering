import numpy as np
import matplotlib.pyplot as plt
import os.path as path
import scipy.optimize as opt


def liner(x, a):
    return a * x


def loglogarea(input_directory, start_frame, end_frame, video_name):
    input_directory = path.join(input_directory, 'area_results')
    output_directory = input_directory

    data = np.loadtxt(path.join(input_directory, 'area_data.txt'))
    frames = list(data[0])[start_frame:end_frame]
    areas = list(data[1])[start_frame:end_frame]

    plt.loglog(frames, areas, label='area')
    plt.xlabel('frame number')
    plt.ylabel('area (in pixels)')
    plt.title('loglog area ' + video_name)

    # Curve Fitting
    xdata = np.log10(frames)
    ydata = np.log10(areas)

    optimized_parameters, pcov = opt.curve_fit(liner, xdata, ydata)

    residuals = ydata - liner(xdata, *optimized_parameters)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    plt.plot(xdata, liner(xdata, *optimized_parameters), label='fit, a = ' + str(pcov) + ', rs = ' + str(r_squared))

    plt.legend(loc='upper left')
    plt.savefig(output_directory + '/loglogarea.pdf')
    plt.show()

    plt.close()


def area_by_per(input_directory, start_frame, end_frame, video_name):
    data = np.loadtxt(path.join(input_directory, 'area_results', 'area_data.txt'))
    areas = list(data[1])[start_frame:end_frame]

    data = np.loadtxt(path.join(input_directory, 'preimiter_results', 'perimiter_data.txt'))
    frames = list(data[0])[start_frame:end_frame]
    pers = list(data[1])[start_frame:end_frame]

    plt.scatter(frames, list(np.divide(areas, pers)), label='area/per')
    plt.xlabel('frame number')
    plt.ylabel('area/per (in pixels)')
    plt.title('area/per ' + video_name)

    # Curve Fitting
    xdata = frames
    ydata = list(np.divide(areas, pers))

    optimized_parameters, pcov = opt.curve_fit(liner, xdata, ydata)

    residuals = ydata - liner(xdata, *optimized_parameters)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    plt.plot(xdata, liner(xdata, *optimized_parameters), label='fit, a = ' + str(pcov) + ', rs = ' + str(r_squared))

    plt.legend(loc='upper left')

    plt.savefig(path.join(input_directory, 'area_results', 'area_div_per.pdf'))
    plt.show()

    plt.close()


video_names = ['video3_001', 'video5_003', 'video6_001', 'video7_001', 'video8_001', 'video9_001', 'video10_001', 'video11_001']
video_start = [0, 0, 0, 0, 0, 0, 0, 0]
video_end = [0, 0, 0, 0, 0, 0, 0, 0]

for i in range(len(video_names)):
    video_name = video_names[i]
    print('\n####### Working on: ' + video_name + ' #######')
    input_directory = '/Users/rotemmayo/Documents/AdvLabFVF/176lab/' + video_name + '_results'

    loglogarea(input_directory, video_start[i], video_end[i], video_name)
    area_by_per(input_directory, video_start[i], video_end[i], video_name)
