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


@click.command(
    help='Image Converter',
    context_settings=dict(help_option_names=['-h', '--help']),
)
@click.option('-i', '--interactive', is_flag=True, help='start interactive image converter')
@click.option('-f', '--file_paths', 'files', required=False, type=str, help='path of the file you want to convert')
@click.option('-d', '--dest_dir', required=False, type=str, help='path of destination directory')
@click.option('-t', '--output_type', 'out_type', required=True, type=click.Choice(['JPG', 'PNG', 'ICO']), default='PNG')
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
        separated = [f.rsplit('/', 1)[1].split('.') for f in files]
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

    # convert images
    stdlog(LOG_INFO, 'Converting images...')
    for f, s in tqdm(zip(files, separated)):
        filename = s[0]
        ext = s[1]
        path = '{dir}/{file}.{ext}'.format(dir=dest_dir,
                                           file=filename, ext=ext)
        if ext == 'svg':
            path_png = '{dir}/{file}.{ext}'.format(
                dir=dest_dir, file=filename, ext='png')
            try:
                svg2png(url=f, write_to=path_png,
                        output_width=512, output_height=512, scale=2.0)
            except IOError:
                stdlog(LOG_ERROR, 'Failed to convert image (SVG to PNG): {}'.format(f))
            if out_type != 'PNG':
                try:
                    img = Image.open(path_png)
                    img.save(path, out_type)
                    os.remove(path_png)
                except IOError:
                    stdlog(LOG_ERROR, 'Failed to convert image: {}'.format(f))
        else:
            try:
                img = Image.open(f)
                img.save(path, out_type)
            except IOError:
                stdlog(LOG_ERROR, 'Failed to convert image: {}'.format(f))

    # end
    stdlog(LOG_INFO, 'Image conversion was successfully completed.')
