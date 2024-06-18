import os
import re
import glob
import datetime
import shutil
import json
import logging

import tomllib
from util.dither import Ditherer


dt = datetime.datetime.now()
logging.basicConfig(level=logging.DEBUG)

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
def parse_front_matter(file_content:str, fmformat:str='.toml',content_format='.md') -> (str, str):
    """ reads file contents and splits out header-level data from content """
    if fmformat == '.toml':
        pattern = r'\+\+\+\s*\n(.*?)\n\+\+\+\n(.*)'
        try:
            match = re.search(pattern, file_content, re.DOTALL)
            return tomllib.loads(match.group(1)), match.group(2)
        except AttributeError as err:
            print(f'Something went wrong parsing front_matter: {err}')

            
def parse_markdown_content(content:str) -> str:
    pass


def replace_placeholders(text, **replacements):
    # Regular expression pattern to match {{ tag_name }} with optional spaces
    pattern = re.compile(r'\{\{\s*(\w+)\s*\}\}')

    # function to replace matched patterns
    def replace_match(match):
        tag_name = match.group(1)
        return replacements.get(tag_name, f'{{{{ {tag_name} }}}}')

    # replace using the pattern and replacement function
    result = re.sub(pattern, replace_match, text)
    return result
        

def main():
    # create a new directory for the site 
    if os.path.isdir('_site'):
        shutil.rmtree('_site')
    shutil.copytree('static', '_site')
    os.mkdir('_site/assets')

    # generate the home_page 
    master_layout = read_file('layout/master.html')
    article_list_layout = read_file('layout/article_list.html')
    cover_layout = read_file('layout/cover.html')
    content_dir = 'content'
    index_route = '_site/index.html'
    home_page_entries = ''
    cover_content = ''

    d = Ditherer(content_dir, '_site/assets')
    d.walk_through_dither()
    
    # TODO remove any potential redundant file entries.
    """ walk through directories recursively and apply dithering."""
    for root, dirs, files in os.walk(os.path.relpath(content_dir), topdown=True):
        dirs.sort()
        logging.info(f'Beginning process for {root}')

        # assuming one .md file per directory
        try:
            md_file = [f for f in files if f.endswith('.md')][0]
        except:
            logging.info(f'No .md file found in {root}. Moving to next directory.')
            continue

        fname, ext = os.path.splitext(md_file)
        article_file_output = os.path.join('_site/articles', fname + '.html')

        # split the md into front matter and content
        article_front_matter, article_content = parse_front_matter(read_file(os.path.join(root,md_file)))

        # for now the about becomes the cover, switch to option for date-based.
        if ('about' not in root and '7' not in root):            
            home_page_entries += replace_placeholders(article_list_layout, **article_front_matter)
        else:
            cover_content += replace_placeholders(cover_layout, **article_front_matter)

    home_page_content = replace_placeholders(master_layout, layout_content= cover_content+ home_page_entries)
    write_file(index_route, home_page_content)
    

main()
