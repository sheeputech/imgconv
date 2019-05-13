import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from cairosvg import svg2png
from tqdm import tqdm
import click

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


@click.command(help='Image Converter', context_settings=dict(help_option_names=['-h', '--help']),)
@click.option('-i', '--interactive', is_flag=True, help='Start interactive image converter.')
@click.option('-f', '--file_paths', 'files', required=False, type=str, help='Path of files you want to convert.')
@click.option('-d', '--dest_dir', required=False, type=str, help='Path of destination directory.')
@click.option('-t', '--output_type', 'out_type', required=False, type=click.Choice(['JPEG', 'PNG', 'ICO']), default='PNG', help='File format to which the target images converted.', show_default=True)
@click.pass_context
def main(ctx, interactive, files, dest_dir, out_type):
    # show help by default
    if (not interactive) & (files == None):
        print(ctx.get_help())
        ctx.exit()

    # start
    stdlog(LOG_INFO, 'Image Converter start running.')
    root = tk.Tk()
    root.withdraw()

    # select target files
    if interactive or (files == None):
        stdlog(LOG_INFO, 'Select target files.')
        files = filedialog.askopenfilenames(
            filetypes=[('image files', ('.svg', '.jpg', '.png'))]
        )
    if len(files) == 0:
        stdlog(LOG_INTERRUPT, 'Image converter interrupted.')
        ctx.exit()

    stdlog(LOG_INFO, 'Selected files are...')
    for i, f in enumerate(files):
        print('{index}. {filename}'.format(index=i + 1, filename=f))

    # select output directory
    if interactive or (dest_dir == None):
        stdlog(LOG_INFO, 'Select destination directory.')
        dest_dir = filedialog.askdirectory()
    if not dest_dir:
        stdlog(LOG_ERROR, 'Image converter was interrupted.')
        ctx.exit()
    stdlog(LOG_INFO, 'Destination directory is : {dir}'.format(dir=dest_dir))

    # set format
    out_format = 'png'
    if out_type == 'JPEG':
        out_format = 'jpg'
    elif out_type == 'ICO':
        out_format = 'ico'

    # convert images
    stdlog(LOG_INFO, 'Converting images...')
    separated = [f.rsplit('/', 1)[1].split('.') for f in files]
    for f, s in tqdm(list(zip(files, separated))):
        filename = s[0]
        ext = s[1]
        path = '{}/{}.{}'.format(dest_dir, filename, out_format)

        if ext == 'svg':
            path_png = '{}/{}.{}'.format(dest_dir, filename, 'png')
            try:
                svg2png(url=f, write_to=path_png,
                        output_width=512, output_height=512, scale=2.0)
            except IOError:
                stdlog(LOG_ERROR, 'Failed to convert image (SVG to PNG): {}'.format(f))
            if out_type != 'PNG':
                try:
                    img = Image.open(path_png)
                    img.save(path, out_format)
                    os.remove(path_png)
                except IOError:
                    stdlog(LOG_ERROR, 'Failed to convert image: {}'.format(f))
        else:
            try:
                img = Image.open(f)
                img.save(path, out_format)
            except IOError:
                stdlog(LOG_ERROR, 'Failed to convert image: {}'.format(f))

    # end
    stdlog(LOG_INFO, 'Image conversion finished.')
