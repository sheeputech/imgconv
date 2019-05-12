import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from cairosvg import svg2png
from tqdm import tqdm

LOG_INFO = 0
LOG_ERROR = 1
LOG_INTERRUPT = 2


def stdlog(type, message):
    if type == 0:
        print('| info:', message)
    elif type == 1:
        print('| error:', message)
    elif type == 2:
        print('| interrupt:', message)


def main():
    stdlog(LOG_INFO, 'Image Converter start running.')

    # setup tkinter
    root = tk.Tk()
    root.withdraw()

    # get files
    stdlog(LOG_INFO, 'Choose PNG files converted.')

    files = filedialog.askopenfilenames(filetypes=[('SVG', '*.svg')])
    if not files:
        stdlog(LOG_INTERRUPT, 'Image converter interrupted.')
        sys.exit()

    stdlog(LOG_INFO, 'Chosen files are...')

    for i, f in enumerate(files):
        print('{index}. {filename}'.format(index=i + 1, filename=f))

    # get output directory
    stdlog(LOG_INFO, 'Choose output directory.')

    out_dir = filedialog.askdirectory()
    if not out_dir:
        stdlog(LOG_ERROR, 'Image converter was interrupted.')
        sys.exit()

    stdlog(LOG_INFO, 'Output directory is : {dir}'.format(dir=out_dir))

    # get PNG and ICO filenames
    png_files = [
        '{out_dir}/{filename}.png'.format(out_dir=out_dir, filename=f.rsplit('/', 1)[1].split('.')[0]) for f in files
    ]
    ico_files = [
        '{path}.ico'.format(path=f.rsplit('.')[0]) for f in png_files
    ]

    # SVG to PNG
    stdlog(LOG_INFO, 'Converting from SVG to PNG temporarily...')

    for f, p in tqdm(list(zip(files, png_files))):
        try:
            svg2png(
                url=f, write_to=p, output_width=512, output_height=512, scale=2.0)
        except IOError:
            stdlog(LOG_ERROR, 'Failed to convert SVG to PNG: {}'.format(f))

    # PNG to ICO
    stdlog(LOG_INFO, 'Converting from PNG to ICO...')

    for p, i in tqdm(list(zip(png_files, ico_files))):
        try:
            img = Image.open(p)
            img.save(i, "ICO")
        except IOError:
            stdlog(LOG_ERROR, 'Failed to convert PNG to ICO: {}'.format(p))

    # remove temp PNG
    stdlog(LOG_INFO, 'Removing temporary PNG files...')

    for p in tqdm(png_files):
        if os.path.isfile(p):
            os.remove(p)

    stdlog(LOG_INFO, 'Image conversion was successfully completed.')


if __name__ == '__main__':
    main()
