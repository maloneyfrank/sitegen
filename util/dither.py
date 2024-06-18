"""
Modified version of dither_images.py
https://github.com/lowtechmag/solar_v2/blob/main/utils/dither_images.py
2022 Roel Roscam Abbing, released as AGPLv3

Modified for further customization later.


2024 Franklin Maloney , released as AGPLv3
# see https://www.gnu.org/licenses/agpl-3.0.html
"""


from PIL import Image, ImagePalette
import hitherdither
import shutil
import logging
import argparse
import os

# custom libraries
from util.parsing import parse_front_matter

logging.basicConfig(level=logging.INFO)

class Ditherer:
    # TODO: move this into config so that user can set this.
    
    palette_dict = {
        'physical-things': hitherdither.palette.Palette([
            (51, 88, 229),
            (15, 57, 178),
            (84, 122, 235),
            (189, 202, 246),
            (215, 219, 250),
            (243, 244, 250)

        ]),
        'digital-things': hitherdither.palette.Palette([
            (255, 111, 66),
            (255, 74, 29),
            (255, 128, 81),
            (255, 183, 152),
            (255, 203, 184),
            (255, 229, 218)
        ]),

        # https://mycolor.space/?hex=%23F7B801
        'favorite-things': hitherdither.palette.Palette([
            (247, 184, 1),   # #F7B801
            (198, 142, 0),   # #C68E00
            (151, 103, 0),   # #976700
            (108, 66, 0),    # #6C4200
            (73, 30, 0)      # #491E00
        ]),
        
        'grayscale': hitherdither.palette.Palette([(25,25,25), (75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250)])
        
    }
    image_ext = [".jpg", ".JPG", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp"]
    content_ext = [".md"]
    exclude_dirs = {'dithers'}


    def __init__(self, content, output):
        self.output_path = output
        self.content_dir = content


    @staticmethod
    def dither_img(source, output, category='grayscale'):
        """ saves a dithered and colorized version of image to output path"""
        try:
            img= Image.open(source).convert('RGB')
            img.thumbnail((800,800), Image.LANCZOS)
            threshold = [96, 96, 96]
            dithered = hitherdither.ordered.bayer.bayer_dithering(img, Ditherer.palette_dict[category], threshold, order=8) 

            dithered.save(output, optimize=True)

        except Exception as e:
            logging.debug(e)


    # TODO remove any potential redundant file entries.
    """ walk through directories recursively and apply dithering."""
    def walk_through_dither(self):
        for root, dirs, files in os.walk(os.path.relpath(self.content_dir), topdown=True):
            logging.info(f'Beginning process for {root}')

            dirs[:] = [d for d in dirs if d not in Ditherer.exclude_dirs]

            if files:
                img_files = [f for f in files if os.path.splitext(f)[1] in Ditherer.image_ext]
                if len(img_files) == 0:
                    logging.info(f'No images in {root}, skipping dir.')
                    continue
                if not os.path.exists(os.path.join(self.output_path,'dithers')):
                    os.mkdir(os.path.join(self.output_path,'dithers'))
                    logging.info(f'dir:dithers created in {self.output_path}')
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
                output_path = os.path.join(os.path.join(self.output_path, 'dithers'), fname + '_dithered.png')

                if os.path.exists(output_path):
                    logging.info(f'{output_path} already exists, skipping.')
                    continue

                Ditherer.dither_img(source_path, output_path, category)
                logging.info("converted {}".format(f))


        
        
