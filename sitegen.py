import os
import re
import glob
import datetime
import shutil
import json
import logging

import tomllib
from util.dither import Ditherer

from util.parsing import *


dt = datetime.datetime.now()
logging.basicConfig(level=logging.DEBUG)


def main():
    # create a new directory for the site 
    if os.path.isdir('_site'):
        shutil.rmtree('_site')
    shutil.copytree('static', '_site')
    os.mkdir('_site/assets')

    # read layout files
    master_layout = read_file('layout/master.html')

    file_path_conversions = {
        '../static/*', '*',
    }

    
    article_list_layout = read_file('layout/article_list.html')
    article_list_item_layout = read_file('layout/article_list_item.html')
    article_layout = read_file('layout/article.html')
    cover_layout = read_file('layout/cover.html')

    # set basic params for generation
    content_dir = 'content'
    index_route = '_site/index.html'
    home_page_entries = ''
    cover_content = ''

    # dither all images for use in site
    d = Ditherer(content_dir, '_site/assets')
    d.walk_through_dither()
    
    # TODO remove any potential redundant file entries.
    """ walk through directories recursively and generate content"""
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
            home_page_entries += replace_placeholders(article_list_item_layout, **article_front_matter)
        else:
            cover_content += replace_placeholders(cover_layout, **article_front_matter)

    
        article_content = replace_placeholders(article_layout, layout_content = parse_markdown(article_content), **article_front_matter)
        article_content = replace_placeholders(master_layout, layout_content=article_content)
        write_file(article_file_output, article_content)
    
    article_list = replace_placeholders(article_list_layout, layout_content= cover_content+ home_page_entries)
    home_page_content = replace_placeholders(master_layout, layout_content= article_list)
    write_file(index_route, home_page_content)
    

main()
