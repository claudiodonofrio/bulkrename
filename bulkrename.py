# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 22:50:09 2022

@author: Claudio
"""

from os import listdir, rename
from os.path import isfile, join
from datetime import datetime
from PIL import Image
import click
from tqdm import tqdm

# if you need to map the EXIF codes to a human readable version use:
# from PIL import ExifTags
# a = ExifTags.TAGS


@click.command()
@click.option('--path','-p', default='.',
              help='Path to a folder where you want to rename images. Default is the current directory.')
@click.option('--execute', '-e', is_flag=True, show_default=True, default=False,
              help='A preview (dry run) is created by default to standard output. If the script is called with --execute or -e, files will be renamed without the possibility of undoing.')
@click.option('--suffix', '-s', 
              help='By default files with suffix png, jpg, tif are read. Here you can add an additional extension if needed.')
def newname(path, execute, suffix):
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
        # open image and read EXIF data
        try:
            img=Image.open(filename)
            # do stuff
        except IOError:
            # filename not an image file            
            click.echo(filename + click.style(' -> ', bg="red") + 'not a valid image format')
            continue
        
        exif_data = img._getexif()
        origin_ts = exif_data[36867] #key contains original timestamp
        
        # create new name based on date & time
        # yymmddhhss
        new_file_name = origin_ts.replace(':','')
        new_file_name = new_file_name.replace(' ','')
        new_file_name = new_file_name[2:12] + filename[-4:] # timestamp + suffix
        new_file_name = join(path, new_file_name)          
        name_dict[filename] = new_file_name
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    