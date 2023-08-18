# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 11:46:54 2023

@author: Claudio.Donofrio
"""

from os import listdir, rename
from os.path import isfile, join, getmtime
from collections import OrderedDict
from datetime import datetime
from PIL import Image
import click
import platform
from tqdm import tqdm

# if you need to map the EXIF codes to a human readable version use:
# from PIL import ExifTags
# a = ExifTags.TAGS


__version__  = '0.1.3'

@click.command()
@click.option('--path_in','-i', default='.',
              help='Path to a folder where you want to read images. Default is the current directory.')

@click.option('--path_out','-o', default='.',
              help='Path to a folder where you want to safe the images. Default is the current directory. \n')

@click.option('--move/--copy', default=True,help="""By default move is activated.
              Which means if the path to read and output path is the same, a renaming (move) of files
              is performed in place. You can not 'undo' this operation""")

@click.option('--execute', '-e', is_flag=True, show_default=True, default=False,
              help='A preview (dry run) is created by default to standard output. If the script is called with --execute or -e, files will be renamed without the possibility of undoing.')

@click.option('--suffix', '-s',  default='',
              help='By default files with suffix png, jpg, tif are read. Here you can add an additional extension if needed.')

@click.version_option(
    version=__version__,
    message=(
        f"%(prog)s, %(version)s \n"
        f"Python ({platform.python_implementation()}) {platform.python_version()}"
    ),
)

#def newname(path_in, path_out, move, execute, suffix):
def newname(*args, **kwargs):
    
    print(args)
    print(kwargs)

if __name__ == '__main__':
    newname()
    