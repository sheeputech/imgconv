from cairosvg import svg2png
from PIL import Image
from tkinter import Tk, filedialog as fd
from tqdm import tqdm
import click
import os

LOG_INFO = 0
LOG_ERROR = 1
LOG_INTERRUPT = 2


@click.command(help='Image Converter', context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-i', 'interactive', is_flag=True, help='Start interactive image converter.')
@click.option('-f', 'fs', required=False, type=str, help='Path of files you want to convert.')
@click.option('-d', 'dest', required=False, type=str, help='Path of destination directory.')
@click.option('-t', 'filetype', required=False, type=click.Choice(['JPEG', 'PNG', 'ICO']), default='PNG', help='File format to which the target images converted.', show_default=True)
@click.pass_context
def main(ctx, interactive, fs, dest, filetype):
    # show help by default
    if not interactive and fs == None:
        print(ctx.get_help())
        ctx.exit()

    # start
    log(LOG_INFO, 'imgconv start')
    tk = Tk()
    tk.withdraw()

    # select target files
    if interactive or fs == None:
        log(LOG_INFO, 'Select target files.')
        fs = fd.askopenfilenames(
            filetypes=[('images', ('.svg', '.jpg', '.png'))])

    if len(fs) == 0:
        log(LOG_INTERRUPT, 'Image converter interrupted.')
        ctx.exit()

    log(LOG_INFO, 'Selected files are...')
    [print(f'{i+1}. {f}') for i, f in enumerate(fs)]

    # select output directory
    if interactive or dest == None:
        log(LOG_INFO, 'Select destination directory.')
        dest = fd.askdirectory()

    if not dest:
        log(LOG_ERROR, 'Image converter was interrupted.')
        ctx.exit()

    log(LOG_INFO, f'Destination directory is : {dest}')

    # set format
    outext = 'png'
    if filetype == 'JPEG':
        outext = 'jpg'
    elif filetype == 'ICO':
        outext = 'ico'

    # convert images
    log(LOG_INFO, 'Converting images...')
    separated = [f.rsplit('/', 1)[1].split('.') for f in fs]

    for f, s in tqdm(list(zip(fs, separated))):
        file = s[0]
        ext = s[1]
        path = f'{dest}/{file}.{outext}'

        if ext == 'svg':
            path_png = f'{dest}/{file}.png'
            try:
                svg2png(url=f, write_to=path_png,
                        output_width=512, output_height=512, scale=1.0)
            except IOError:
                log(LOG_ERROR, f'Failed to convert image (SVG to PNG): {f}')

            if filetype != 'PNG':
                try:
                    img = Image.open(path_png)
                    img.save(path, outext)
                    os.remove(path_png)
                except IOError:
                    log(LOG_ERROR, f'Failed to convert image: {f}')
        else:
            try:
                img = Image.open(f)
                img.save(path, outext)
            except IOError:
                log(LOG_ERROR, f'Failed to convert image: {f}')

    # end
    log(LOG_INFO, 'Image conversion finished.')


def log(logtype, message):
    if logtype == LOG_INFO:
        print('| info:', message)
    elif logtype == LOG_ERROR:
        print('| error:', message)
    elif logtype == LOG_INTERRUPT:
        print('| interrupt:', message)
