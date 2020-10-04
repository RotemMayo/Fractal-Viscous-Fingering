from PyPDF2 import PdfFileMerger

video_names = ['video3_001', 'video5_003', 'video6_001', 'video7_001', 'video8_001', 'video9_001', 'video10_001', 'video11_001']
merger = PdfFileMerger()

for video_name in video_names:
    print('\n####### Working on: ' + video_name + ' #######')
    directory = '/Users/rotemmayo/Documents/AdvLabFVF/176lab/' + video_name + '_results'
    pdf_files = ['/preimiter_results/perimiter.pdf',
                 '/area_results/area.pdf',
                 '/area_results/area_div_per.pdf',
                 '/area_results/area_vs_per.pdf',
                 '/area_results/area_vs_per_loglog.pdf',
                 '/area_results/loglogarea.pdf']
    for file in pdf_files:
        merger.append(directory + file)

merger.write('/Users/rotemmayo/Documents/AdvLabFVF/176lab/Full Results.pdf')
merger.close()
