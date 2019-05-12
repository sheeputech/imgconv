from setuptools import setup

setup(
    name='imgconv',
    version='0.0.1',
    description='Convert SVG files to ICO images',
    author='Kazumasa Hirata',
    author_email='sheepu.tech@gmail.com',
    url='https://github.com/sheeputech/imgconv',
    install_require=['cairosvg', 'Pillow', 'tqdm'],
    entry_points={
        'console_scripts': [
            'imgconv = imgconv.imgconv:main'
        ]
    }
)
