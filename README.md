# imgconv
Convert images to another format with Python.  

<small>*\*1: You need to install [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/) before using this image converter.*</small>  
<small>*\*2: If you use Windows, you need to install [GTK+ (The GIMP Toolkit)](http://futago-life.com/wife-support/tech/import-cairosvg-error.html) additionally.*</small>  

## Usage
### Clone repository
```
$ git clone git@github.com:sheeputech/imgconv
```

### Installation
In the repository root directory,
```
$ pip install -e .
```

### Convert your files interactively
```
$ imgconv -i
```
<small>* Default file format is PNG.</small>

## Supporting conversion formats
### from  
- `.svg`
- `.jpg`
- `.png`

### to
- `.jpg`
- `.png`
- `.ico`

## Third Party Dependencies
- [cairosvg](https://cairosvg.org/)
- [Pillow](https://pillow.readthedocs.io/en/latest/)
- [tqdm](https://pypi.org/project/tqdm/)
- [click](https://click.palletsprojects.com/en/7.x/)