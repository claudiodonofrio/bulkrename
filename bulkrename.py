# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 22:50:09 2022

@author: Claudio
"""

from os import listdir, rename
from os.path import isfile, join, getmtime
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
@click.option('--path','-p', default='.',
              help='Path to a folder where you want to read images. Default is the current directory.')
@click.option('--out','-o', default='.',
              help='Path to a folder where you want to safe the images. Default is the current directory. \n')
@click.option('--move/--copy', default=True,help="""By default move is activated.
              Which means if the path to read and output path is the same, a renaming (move) of files
              is performed in place. You can not 'undo' this operation""")

@click.option('--execute', '-e', is_flag=True, show_default=True, default=False,
              help='A preview (dry run) is created by default to standard output. If the script is called with --execute or -e, files will be renamed without the possibility of undoing.')
@click.option('--suffix', '-s', 
              help='By default files with suffix png, jpg, tif are read. Here you can add an additional extension if needed.')
@click.version_option(
    version=__version__,
    message=(
        f"%(prog)s, %(version)s \n"
        f"Python ({platform.python_implementation()}) {platform.python_version()}"
    ),
)

def newname(path, out, move, execute, suffix):
    '''
    This script will rename existing image files based on the creation date
    found in the meta data of the file. If the file does already exist, it will
    be skipped.
    
    By default a dry run is executed to show the outcome of the script.
    For a real execution (renaming the files on the server), you need to set
    the flag --execute. If --execute is set, a logfile 'log.txt' is written
    to the current directory with the performed actions.
    '''
    args = locals()
    
    extensions = ['png', 'jpg', 'tif']
    if suffix:
        extensions.append(suffix.lower())
    
    images = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    
    # if there are files, remove all which do not have the 'right' extension
    if images:        
        images = [i for i in images if i[-3:].lower() in extensions]
    
    
    click.echo('configuration: ')
    click.echo(args)
    click.echo('-------------')
    name_dict = {}
    for filename in tqdm(images):
        
        img = False
        # open image and read EXIF data
        try:
            img=Image.open(filename)
            exif_data = img._getexif()
            origin_ts = exif_data[36867] #key contains original timestamp
            
        except Exception as e:
            # filename not an image file, revert to modification date
            ts = getmtime(filename)
            origin_ts = datetime.fromtimestamp(ts).strftime("%Y%m%d%H%M")
            click.echo(filename + click.style(' -> ', bg="green") + 'not an image, use file modification timestamp')
                
        # create new name based on date & time
        # yymmddhhss
        new_file_name = origin_ts.replace(':','')
        new_file_name = new_file_name.replace(' ','')
        new_file_name = new_file_name[2:12] + filename[-4:] # timestamp + suffix
        new_file_name = join(path, new_file_name)          
        name_dict[filename] = new_file_name
        if img:
            img.close()
        
    if not execute:
        click.echo('dry run')
        click.echo('-------')        
        for k,v in name_dict.items():
            if isfile(v):
                click.echo(k + ' -> ' + v + click.style(' -> ', bg="yellow") + 'skip, exists')
            else:
                click.echo(k + ' -> ' + click.style(v, bg="green", fg='black')) 
        
    if execute:
        log = open("log.txt", "a")
        log.write(str(datetime.now())+'\n')
        log.write(str(args))
        log.write('---------------')
        for k,v in name_dict.items():
            if isfile(v):
                click.echo(k + ' -> ' + v + click.style(' -> ', bg="red") + 'skipped, exists')
                log.write(k + ' -> ' + v + ' -> skipped, exists'+'\n')
                continue
                
            rename(k, v)            
            click.echo(k + ' -> ' + v + click.style(' -> ok' , bg="green"))
            log.write(k + ' -> ' + v + ' -> ok'+'\n')
    
        log.close()

    
if __name__ == '__main__':
    newname()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    