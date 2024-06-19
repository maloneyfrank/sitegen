import re
import tomllib
import markdown
import os


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
    html = markdown.markdown(md_content)
    if wrap_images: html = replace_images_with_figures(html, 'layout/article_image_wrap.html')
    return html
    
def replace_images_with_figures(html: str, img_layout_path:str) -> str:
    """ Optional function to wrap images in figure for captioning, styling, etc."""
    img_layout = read_file(img_layout_path)
    img_pattern = re.compile(r'(<img\s[^>]*>)')
    
    def wrap_figure(match):
        img_tag = match.group(1)
        figure_content = replace_placeholders(img_layout, img_html=img_tag)
        return figure_content
    
    result = img_pattern.sub(wrap_figure, html)
    
    return result

def replace_placeholders(text, **replacements):
    pattern = re.compile(r'\{\{\s*(\w+)\s*\}\}')
    
    def replace_match(match):
        tag_name = match.group(1)
        return replacements.get(tag_name, f'{{{{ {tag_name} }}}}')

    result = re.sub(pattern, replace_match, text)
    return result

