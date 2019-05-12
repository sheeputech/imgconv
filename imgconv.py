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
        print('| info: {message}'.format(message=message))
    elif type == 1:
        print('| error: {message}'.format(message=message))
    elif type == 2:
        print('| interrupt: {message}'.format(message=message))


def main():
    stdlog(LOG_INFO, 'Image Converter start running.')

    # Setup tkinter
    root = tk.Tk()
    root.withdraw()

    # Converted files
    stdlog(LOG_INFO, 'Choose PNG files converted.')
    f_types = [('SVG', '*.svg')]
    init_dir = 'C:\\Users\\kzms9\\Pictures'
    in_files = filedialog.askopenfilenames(filetypes=f_types,
                                           initialdir=init_dir)

    if not in_files:
        stdlog(LOG_INTERRUPT, 'Image converter interrupted.')
        sys.exit()

    stdlog(LOG_INFO, 'Chosen files are...')
    for i, f in enumerate(in_files):
        print('{index}. {filename}'.format(index=i + 1, filename=f))

    # Output directory
    stdlog(LOG_INFO, 'Choose output directory.')
    out_dir = filedialog.askdirectory(initialdir=init_dir)

    if not out_dir:
        stdlog(LOG_ERROR, 'Image converter was interrupted.')
        sys.exit()

    stdlog(LOG_INFO, 'Output directory is : {dir}'.format(dir=out_dir))

    png_files = [
        '{out_dir}/{filename}.png'.format(out_dir=out_dir, filename=f.rsplit('/', 1)[1].split('.')[0]) for f in in_files]
    ico_files = ['{path}.ico'.format(path=f.rsplit('.')[0]) for f in png_files]

    stdlog(LOG_INFO, 'Converting from SVG to PNG')
    for f, p in tqdm(list(zip(in_files, png_files))):
        try:
            svg2png(
                url=f, write_to=p, output_width=512, output_height=512, scale=2.0)
        except IOError:
            stdlog(LOG_ERROR, 'Failed to convert SVG to PNG: {f}'.format(f=f))

    stdlog(LOG_INFO, 'Converting from PNG to ICO')
    for p, i in tqdm(list(zip(png_files, ico_files))):
        try:
            img = Image.open(p)
            img.save(i, "ICO")
        except IOError:
            stdlog(LOG_ERROR, 'Failed to convert PNG to ICO: {f}'.format(f=f))

    stdlog(LOG_INFO, 'Removing temporary PNG files.')
    for f in png_files:
        if os.path.isfile(f):
            os.remove(f)

    stdlog(LOG_INFO, 'Image conversion was successfully completed.')


if __name__ == '__main__':
    main()
