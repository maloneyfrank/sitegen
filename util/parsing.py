import re
import tomllib
import markdown
import os
import logging

logging.basicConfig(level=logging.INFO)


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

def parse_front_matter(file_content:str, format='toml') -> (str, str):
    """ reads file contents and splits out header-level data from content """
    if format == 'toml':
        pattern = r'\+\+\+\s*\n(.*?)\n\+\+\+\n(.*)'
        try:
            match = re.search(pattern, file_content, re.DOTALL)
            return tomllib.loads(match.group(1)), match.group(2)
        except AttributeError as err:
            print(f'Something went wrong parsing front_matter: {err}')


def parse_markdown(md_content:str, wrap_images=True) -> str:
    """ markdown to html with optional additional operations"""
    html = markdown.markdown(md_content)
    if wrap_images: html = replace_images_with_figures(html, 'layout/article_image_wrap.html')
    return html


def replace_images_with_figures(html: str, img_layout_path:str) -> str:
    """
    Function to wrap images in figure for captioning, styling, etc.
    Assumes that line of text under the image is the caption.
    Requires a caption right now.
    """
    img_layout = read_file(img_layout_path)
    img_pattern = re.compile(r'<p>(<img\s[^>]*>)\s*(.*?)</p>', re.DOTALL)

    def wrap_figure(match):
        img_tag, caption = match.groups()  # Extract img tag and caption directly
        caption = caption.strip()
        figure_content = replace_placeholders(img_layout, img_html=img_tag, caption=caption)
        return figure_content
    
    result = img_pattern.sub(wrap_figure, html)
    return result

def replace_placeholders(text, **replacements):
    """ takes page layout and substitutes in for variable expression."""    
    pattern = re.compile(r'\{\{\s*(\w+)\s*\}\}')
    
    def replace_match(match):
        tag_name = match.group(1)
        return replacements.get(tag_name, f'{{{{ {tag_name} }}}}')

    result = re.sub(pattern, replace_match, text)
    return result



def replace_file_paths(html: str, replacements: dict) -> str:
    """
    takes in a dict of file paths to replace
    TODO: make more opinionated about file structuring
    """
    pattern = re.compile(r'(src|href)=["\']([^"\']+)["\']')
    
    def replace_match(match):
        attribute = match.group(1)
        file_path = match.group(2)
        new_file_path = replacements.get(file_path, file_path)
        return f'{attribute}="{new_file_path}"'

    result = re.sub(pattern, replace_match, html)
    return result


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]
