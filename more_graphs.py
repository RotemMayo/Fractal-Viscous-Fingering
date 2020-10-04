import numpy as np
import matplotlib.pyplot as plt
import os.path as path
import scipy.optimize as opt


def liner(x, a):
    return np.multiply(x, a)


def power(x, a, b):
    return np.multiply(np.power(x, b), a)


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
    try:
        xdata = frames
        ydata = areas

        optimized_parameters, pcov = opt.curve_fit(power, xdata, ydata)

        residuals = ydata - power(xdata, *optimized_parameters)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        plt.loglog(xdata, power(xdata, *optimized_parameters), label='fit')
        text = 'a = {:.5f}, b = {:.3f}, rs = {:.3f}'.format(optimized_parameters[0], optimized_parameters[1], r_squared)
        plt.figtext(0.99, 0.01, text, horizontalalignment='right')
    except RuntimeError as e:
        print(e)

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

    # # Curve Fitting
    # xdata = frames
    # ydata = list(np.divide(areas, pers))
    #
    # optimized_parameters, pcov = opt.curve_fit(liner, xdata, ydata)
    #
    # residuals = ydata - liner(xdata, *optimized_parameters)
    # ss_res = np.sum(residuals ** 2)
    # ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
    # r_squared = 1 - (ss_res / ss_tot)
    #
    # plt.plot(xdata, liner(xdata, *optimized_parameters), label='fit, a = ' + str(optimized_parameters) + ', rs = ' + str(r_squared))

    plt.legend(loc='upper right')

    plt.savefig(path.join(input_directory, 'area_results', 'area_div_per.pdf'))
    plt.show()

    plt.close()


def area_vs_per(input_directory, start_frame, end_frame, video_name):
    data = np.loadtxt(path.join(input_directory, 'area_results', 'area_data.txt'))
    areas = list(data[1])[start_frame:end_frame]

    data = np.loadtxt(path.join(input_directory, 'preimiter_results', 'perimiter_data.txt'))
    pers = list(data[1])[start_frame:end_frame]

    plt.loglog(areas, pers)
    plt.xlabel('area')
    plt.ylabel('per')
    plt.title('area vs per loglog' + video_name)

    plt.legend(loc='upper right')
    plt.savefig(path.join(input_directory, 'area_results', 'area_vs_per_loglog.pdf'))
    plt.show()
    plt.close()


def lla_vs_p_slope(input_directory, start_frame, end_frame, video_name):
    data = np.loadtxt(path.join(input_directory, 'area_results', 'area_data.txt'))
    areas = list(data[1])[start_frame:end_frame]

    data = np.loadtxt(path.join(input_directory, 'preimiter_results', 'perimiter_data.txt'))
    frames = list(data[0])[start_frame:end_frame]
    pers = list(data[1])[start_frame:end_frame]

    lareas = np.log10(areas)
    lpers = np.log10(pers)

    slopes = []
    for j in range(len(lareas) - 1):
        dp = lpers[j + 1] - lpers[j]
        da = lareas[j + 1] - lareas[j]
        slopes = slopes + [dp / da]

    frames = frames[:-1]

    plt.loglog(frames, slopes)
    plt.xlabel('frame')
    plt.ylabel('slope')
    plt.title('llavp slope vs frame ' + video_name)

    plt.legend(loc='upper right')
    plt.savefig(path.join(input_directory, 'area_results', 'llavsp slope.pdf'))
    plt.show()
    plt.close()


def lla_slope_by_pressure():
    bars = [0.05, 0.15, 0.2, 0.25, 0.3,  0.4]
    slopes = [1.892, 1.976, 1.935, 2.795, 4.366, 4.366]

    plt.scatter(bars, slopes)
    plt.xlabel('bar')
    plt.ylabel('log log area fit slope')
    plt.title('Slope by Pressure')

    plt.show()


def hd_by_pressure():
    bars = [0.05, 0.15, 0.2, 0.25, 0.3, 0.4, 0.45]
    hds = [1.645455152710791, 1.6382462120740486, 1.6477028875919444, 1.64054654307606, 1.620708733463179, 1.6421548247385906,  1.5892127080414984]

    plt.scatter(bars, hds)
    plt.xlabel('bar')
    plt.ylabel('hd')
    plt.title('Final Hausdorff dimension by Pressure')

    plt.show()


video_names = ['video3_001', 'video5_003', 'video6_001', 'video7_001', 'video8_001', 'video9_001', 'video10_001', 'video11_001']
# TODO this is the index of the frame itself, but indexing in the functions start from zero!
video_start = [2720,            237,        163,            256,        328,            1319,       242,            472]
video_end =   [4501,            757,        539,            528,        603,            1503,       362,            584]

for i in range(len(video_names)):
    video_name = video_names[i]
    print('\n####### Working on: ' + video_name + ' #######')
    input_directory = '/Users/rotemmayo/Documents/AdvLabFVF/176lab/' + video_name + '_results'

    # loglogarea(input_directory, video_start[i], video_end[i], video_name)
    # area_by_per(input_directory, video_start[i], video_end[i], video_name)
    # area_vs_per(input_directory, video_start[i], video_end[i], video_name)

    # lla_slope_by_pressure()
    # lla_vs_p_slope(input_directory, video_start[i], video_end[i], video_name)
    hd_by_pressure()