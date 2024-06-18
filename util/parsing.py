import re
import tomllib

def parse_front_matter(file_content:str, format='toml') -> (str, str):
    """ reads file contents and splits out header-level data from content """
    if format == 'toml':
        pattern = r'\+\+\+\s*\n(.*?)\n\+\+\+\n(.*)'
        try:
            match = re.search(pattern, file_content, re.DOTALL)
            return tomllib.loads(match.group(1)), match.group(2)
        except AttributeError as err:
            print(f'Something went wrong parsing front_matter: {err}')

            
