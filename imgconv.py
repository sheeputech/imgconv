import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from cairosvg import svg2png
from tqdm import tqdm

if __name__ == '__main__':
    print('Image converter start.')

    # Setup tkinter
    root = tk.Tk()
    root.withdraw()

    # Converted files
    print('1. Choose PNG files converted.')
    f_types = [('SVG', '*.svg')]
    init_dir = 'C:\\Users\\kzms9\\Pictures'
    in_files = filedialog.askopenfilenames(filetypes=f_types,
                                           initialdir=init_dir)

    if not in_files:
        print('Image converter interrupted.')
        sys.exit()

    print('Chosen files are...')
    for i, f in enumerate(in_files):
        print('{index}. {filename}'.format(index=i + 1, filename=f))

    # Output directory
    print('2. Choose output directory.')
    out_dir = filedialog.askdirectory(initialdir=init_dir)

    if not out_dir:
        print('Image converter was interrupted.')
        sys.exit()

    print('Output directory is : {dir}'.format(dir=out_dir))

    png_files = [
        '{out_dir}/{filename}.png'.format(out_dir=out_dir, filename=f.rsplit('/', 1)[1].split('.')[0]) for f in in_files]
    ico_files = ['{path}.ico'.format(path=f.rsplit('.')[0]) for f in png_files]

    print('Converting from SVG to PNG')
    for f, p in tqdm(list(zip(in_files, png_files))):
        try:
            svg2png(
                url=f, write_to=p, output_width=512, output_height=512, scale=2.0)
        except IOError:
            print('Failed to convert SVG to PNG:', f)

    print('Converting from PNG to ICO')
    for p, i in tqdm(list(zip(png_files, ico_files))):
        try:
            img = Image.open(p)
            img.save(i, "ICO")
        except IOError:
            print('Failed to convert PNG to ICO:', f)

    print('Removing temporary PNG files.')
    for f in png_files:
        if os.path.isfile(f):
            os.remove(f)

    print('Image conversion was successfully completed.')
