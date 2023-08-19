# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 22:50:09 2022

@author: Claudio
"""
import sys
import shutil
from os import listdir
from os.path import isfile, join, getmtime, isdir, abspath
from datetime import datetime
from PIL import Image
import click
import platform
from tqdm import tqdm

# if you need to map the EXIF codes to a human readable version use:
# from PIL import ExifTags
# a = ExifTags.TAGS


__version__  = '0.1.4'
quiet = True

@click.command(add_help_option=True, no_args_is_help=False, hidden=False, deprecated=False)
@click.option('--src','-s', default='.',
              help='Path to a folder where you want to read images. Default is the current directory.')

@click.option('--dest','-d', default='.',
              help='Path to a folder where you want to safe the images. Default is the current directory. \n')

@click.option('--move/--copy', '-m/-c', default=True,help="""By default move is activated.
              Which means if the path to read and output path is the same, a renaming (move) of files
              is performed in place. You can not 'undo' this operation""")

@click.option('--execute', '-e', is_flag=True, show_default=True, default=False,
              help='A preview (dry run) is created by default to standard output. If the script is called with --execute or -e, files will be renamed without the possibility of undoing.')

@click.option('--suffix', '-x',
              help='By default files with suffix png, jpg, tif are read. Here you can add an additional extension if needed.')

@click.option('--nologfile', '-n', is_flag=True, show_default=True, default=False,
              help='By default a logfile is written to the destination folder (--src, -s), if -e --executed is set')

@click.option('--quiet', '-q', is_flag = True, default=False, help='By default actions are written to standard output.')

@click.version_option(
    version=__version__,
    message=(
        f"%(prog)s, %(version)s \n"
        f"Python ({platform.python_implementation()}) {platform.python_version()}"
    ),
)

def newname(**kwargs):
    '''
    This script will rename existing image files based on the creation date
    found in the meta data of the file. 
    
    You can provide an additional suffix, for files you would like to rename
    to complement existing the existing list of png, jpg, tif. If any of the 
    files do not contain metadata, the script will use the modification date
    for the new name.

    By default a dry run is executed to show the outcome of the script.
    For a real execution (renaming the files on the server), you need to set
    the flag --execute. If --execute is set, a logfile 'log.txt' is written
    to the destination directory with the performed actions.
    
    \n
    The simplest command would be to have a dry run to rename all images in the current folder    
    \n
    bulkrename -s . -d .
         
    \n
    if you want to execute to command for real, you MUST provide the execution flag    
    \n
    bulkrename --execute -src . -dest .
    '''

    global quiet
    quiet = kwargs['quiet']
    console('configuration:')
    for k,v in kwargs.items():
        console(f'{k} : {v}')
    console('-------------')
    
        
    if not __sanity__(kwargs):        
        return sys.exit(1)

    extensions = ['png', 'jpg', 'tif']
    if kwargs['suffix']:
        extensions.append(kwargs['suffix'].lower())

    images = [join(kwargs['src'], f) for f in listdir(kwargs['src']) if isfile(join(kwargs['src'], f))]

    # if there are files, remove all which do not have the 'right' extension
    if images:
        images = [i for i in images if i[-3:].lower() in extensions]


    name_dict = {}
    for filename in tqdm(images):
        
        #lets deal with absolute filenames, makes the logfile more meaningful
        
        filename = abspath(filename)

        img = False
        # open image and read EXIF data
        try:
            img=Image.open(filename)
            exif_data = img._getexif()
            origin_ts = exif_data[36867] #key contains original timestamp

        except Exception as e:
            # filename not an image file, revert to modification date, but            
            ts = getmtime(filename)
            console(e)
            origin_ts = datetime.fromtimestamp(ts).strftime("%Y%m%d%H%M")
            console(filename + click.style(' -> ', bg="green") + 'use file modification timestamp')

        # create new name based on date & time
        # yymmddhhss
        new_file_name = origin_ts.replace(':','')
        new_file_name = new_file_name.replace(' ','')
        new_file_name = new_file_name[2:12] + filename[-4:] # timestamp + suffix
        new_file_name = join(kwargs['dest'], new_file_name)
        new_file_name = abspath(new_file_name)        
        name_dict[filename] = new_file_name
        if img:
            img.close()

    if not kwargs['execute']:
        console(click.style('dry run',bg="green") + ', set --execute to process the files')
        console('-------')
        for k,v in name_dict.items():
            if isfile(v):
                console(k + ' -> ' + v + click.style(' -> ', bg="yellow") + 'skip, exists')
            else:
                console(k + ' -> ' + click.style(v, bg="green", fg='black'))

    if kwargs['execute']:
        console(click.style('execution started',bg="green"))
        logtxt = ''
        logtxt += f'---- start of log --------- {datetime.now()}\n'
        for k,v in kwargs.items():
            logtxt += f'{k} : {v}\n'
        logtxt += f'extensions: {str(extensions)}\n'
        logtxt += '-------------- -----------\n'
        
        ''' now we move or copy the files
            
        if move = True
            this is equivalent to rename. If path in and out
            are the same, the original file is renamed. This can not be undone.
            You could use the log.txt file to manually reverse.
        
        if move = False a copy of the file is created with the new name.
        
        for both options, if the the destination files exists already, 
        it will be skipped.        
        '''
        for k,v in name_dict.items():
            if isfile(v):
                console(k + ' -> ' + v + click.style(' -> ', bg="red") + 'skipped, exists')
                logtxt += f'{k} -> {v} -> skipped, exists\n'                
                continue

            if kwargs['move']:
                shutil.move(k, v)
            else:                
                shutil.copy2(k, v)
            
            console(k + ' -> ' + v + click.style(' -> ok' , bg="green"))
            logtxt += f'{k} -> {v}\n'

        logtxt += f'---- end of log ----------- {datetime.now()}\n'
        write_log(logtxt, kwargs)

def console(msg=None):    
    if not quiet:
        click.secho(msg)

def write_log(logtxt, kwargs):
    if not kwargs['nologfile']:
        logfile = join(kwargs['dest'], 'log.txt')     
        log = open(logfile, "a")
        log.write(logtxt)        
        log.close()
        console(f'log written to: {logfile}')

def __sanity__(args, console=True):
    ''' check for valid entries provided to the main funciton
        returns TRUE if all checks are valid, otherwise FALSE
        console = TRUE prints failed tests to standard output
        console = FALSE, stay quiet        
    '''
    
    sanity = True
    if not isdir(args['src']):
        sanity = False
        console(f"{args['src']} not found")
        
    if not isdir(args['dest']):
        sanity = False
        console(f"{args['dest']} not found'")
    
    return sanity

if __name__ == '__main__':
    newname()




















