import os
import re
import glob
import datetime
import shutil
import json
import logging

import tomllib

dt = datetime.datetime.now()

# TODO: expand to be compatible with more types.
def read_file(filename: str) -> str:
    """ reads file to string """
    with open(filename, 'r') as f:
        return f.read()


def write_file(filename: str, val: str) -> None:
    """ write content to file """
    basedir = os.path.dirname(filename)
    if not os.path.isdir(basedir):
        os.makedirs(basedir)

    with open(filename, 'w') as f:
        f.write(val)


# TODO add JSON.

def parse_front_matter(file_content:str, format='toml') -> (str, str):
    """ reads file contents and splits out header-level data from content """
    if format == 'toml':
        pattern = r'\+\+\+\s*\n(.*?)\n\+\+\+\n(.*)'
        try:
            match = re.search(pattern, file_content, re.DOTALL)
            return tomllib.loads(match.group(1)), match.group(2)
        except AttributeError as err:
            print(f'Something went wrong parsing front_matter: {err}')

            
    
def replace_placeholders(content: str, content_format:str = '.md'):
    
