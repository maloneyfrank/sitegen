"""
Modified version of dither_images.py
https://github.com/lowtechmag/solar_v2/blob/main/utils/dither_images.py
© 2022 Roel Roscam Abbing, released as AGPLv3

Modified for further customization later.


© 2024 Franklin Maloney , released as AGPLv3
# see https://www.gnu.org/licenses/agpl-3.0.html
"""


from PIL import Image, ImagePalette
import hitherdither
import shutil
import logging
import argparse
import os

# custom libraries
from parsing import parse_front_matter

parser = argparse.ArgumentParser(
    """
    Traverses folders and dithers/colorizes images based on
    the folder that they are contained in. Will only dither images
    that have not been dithered before.
    """
)

parser.add_argument(
    '-d', '--directory', help='set the directory', default = '.'
)


parser.add_argument(
    '-o', '--override', help='override existing dithers', action='store_true'
)

parser.add_argument(
    '-c', '--colorize', help='specifies whether to colorize the images', action='store_true'
)

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

# TODO: move this into config so that user can set this.
# IDEA: or infer the color palette from the css somehow.
palette_dict = {
    'physical-things': hitherdither.palette.Palette([(30,32,40), (11,21,71),(57,77,174),(158,168,218),(187,196,230),(243,244,250)]),
    'digital-things': hitherdither.palette.Palette([(9,74,58), (58,136,118),(101,163,148),(144,189,179),(169,204,195),(242,247,246)]),
    'favorite-things': hitherdither.palette.Palette([(86,9,6), (197,49,45),(228,130,124),(233,155,151),(242,193,190),(252,241,240)]),
    'grayscale': hitherdither.palette.Palette([(25,25,25), (75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250)])

}


image_ext = [".jpg", ".JPG", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp"]
content_ext = [".md"]

exclude_dirs = {'dithers'}


# For the PIL version.
# def construct_palette_images(palettes):
#     palette_dict = {}
#     for key, val in palettes.items():
#         flat_pal = [v  for rgb in val for v in rgb]
#         palette_dict[key] = define_palette_image(flat_pal)
#     return palette_dict


# def define_palette_image(palette):
#     """creates an image that can be used to apply palette in dither_img"""
#     palette_image = Image.new('P', (1, 1))
#     palette_image.putpalette(palette)
#     return palette_image



def dither_img(source, output, category='grayscale'):
    try:
        img= Image.open(source).convert('RGB')
        img.thumbnail((800,800), Image.LANCZOS)
        threshold = [96, 96, 96]
        dithered = hitherdither.ordered.bayer.bayer_dithering(img, palette_dict[category], threshold, order=8) 
        
        dithered.save(output, optimize=True)
        
    except Exception as e:
        logging.debug(e)



content_dir = '../content'

""" walk through directories recursively and apply dithering."""
for root, dirs, files in os.walk(os.path.relpath(content_dir), topdown=True):
    logging.info(f'Beginning process for {root}')

    dirs[:] = [d for d in dirs if d not in exclude_dirs]

    if files:
        img_files = [f for f in files if os.path.splitext(f)[1] in image_ext]
        if len(img_files) == 0:
            logging.info(f'No images in {root}, skipping dir.')
            continue
        if not os.path.exists(os.path.join(root,'dithers')):
            os.mkdir(os.path.join(root,'dithers'))
            logging.info(f'dithers 📁 created in {root}')
    else: continue

    category = 'grayscale'
    try:
        md_file = [f for f in files if f.endswith('.md')][0]

        with open(root+'/'+md_file) as f:
            category = parse_front_matter(f.read())[0]['category']

        logging.info(f'Category found as {category}, applying palette.')
            
    except Exception as e:
        logging.info('No file specifying category in this directory. Applying grayscale.')



    # TODO remove redundant text splitting. 
    for f in img_files:
        fname, ext = os.path.splitext(f)
        source_path = os.path.join(root, f)
        output_path = os.path.join(os.path.join(root, 'dithers'), fname + '_dithered.png')
        
        if os.path.exists(output_path) and args.override is False:
            logging.info(f'{output_path} already exists, skipping.')
            continue
        
        dither_img(source_path, output_path, category)
        logging.info("converted {}".format(f))

        
        
        
