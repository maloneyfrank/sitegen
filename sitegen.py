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
from typing import NamedTuple

dt = datetime.datetime.now()
logging.basicConfig(level=logging.DEBUG)

class Layout(NamedTuple):
    """
    Useful abstraction for later functionality that will be added to configuration options.
    i.e. applying options to layout, more privileged keywords, etc.
    also just clear to type layout_name.fill()
    """
    file_path: str
    root_dir: str = '_site/' 


    def __str__(self):
        """
        read and return layout contents as a string.
        """
        return read_file(self.file_path)


    def fill(self, **args)->str:
        """
        fill the layout with specified content and return as string
        """
        return replace_placeholders(self.__str__(),  **args)
        

    def write_layout(self, output_path: str, layout_content: str, **args) -> None:
        """ replace the privileged {{ layout_content }} block and write file."""
        content = replace_placeholders(self.__str__(), layout_content=layout_content, **args)
        write_file(self.root_dir + output_path, content)

        
    
def main():
    # create a new directory for the site 
    if os.path.isdir('_site'):
        shutil.rmtree('_site')
    shutil.copytree('static', '_site')
    os.mkdir('_site/assets')
    
    # set basic params for generation
    content_dir = 'content'
    index_route = '_site/index.html'

    """ These two should be replaced with a new method."""
    home_page_entries = ''
    cover_content = ''

    # Home Page Layouts:
    master_layout = Layout('layout/master.html')
    article_list_layout = Layout('layout/article_list.html')
    article_list_item_layout = Layout('layout/article_list_item.html')
    cover_layout = Layout('layout/cover.html')

    #Article Page Layouts
    article_layout = Layout('layout/article.html')


    # dither all images for use in site
    d = Ditherer(content_dir, '_site/assets')
    d.walk_through_dither()
    
    # TODO remove any potential redundant file entries.
    """ walk through directories recursively and generate content"""
    for root, dirs, files in os.walk(os.path.relpath(content_dir), topdown=True):
        dirs.sort()
        logging.info(f'Beginning process for {root}')

        """
        Assuming one article per folder for now.
        """
        try:
            md_file = [f for f in files if f.endswith('.md')][0]
        except:
            logging.info(f'No .md file found in {root}. Moving to next directory.')
            continue

        fname, ext = os.path.splitext(md_file)

        """
        Extract content and front matter from article and set the path for linking and file write. 
        """
        article_front_matter, article_content = parse_front_matter(read_file(os.path.join(root, md_file)))
        article_path =  'articles/' + article_front_matter['title'].replace(' ', '_').lower() + '.html'

        # article_link is defined in layout to specify link to current article
        article_front_matter['article_link'] = article_path

        """
        TODO: For now, defaulting to have the any article with about in the title to become the pinned/featured article.
        This makes sense in the context of a personal website, but should change this to be a configuration.
        i.e. (about, most_recent_article, keyword) options to determine featured article.
        """
        
        if ('about' not in root):            
            home_page_entries += article_list_item_layout.fill(**article_front_matter)
        else:
            article_path  =  'about.html'
            article_front_matter['article_link'] = article_path
            cover_content += cover_layout.fill(**article_front_matter)

    
        article_content = article_layout.fill(**article_front_matter, layout_content=parse_markdown(article_content))
        master_layout.write_layout(article_path, article_content)
    
    article_list = article_list_layout.fill(layout_content=cover_content + home_page_entries)
    master_layout.write_layout('index.html', article_list)
    

main()
