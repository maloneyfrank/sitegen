"""
Modified version of dither_images.py
https://github.com/lowtechmag/solar_v2/blob/main/utils/dither_images.py
© 2022 Roel Roscam Abbing, released as AGPLv3

This script uses `dithering` library instead of `hitherdither` and determines the colorization
based on the directory path rather than expecting an md file in the same directory.
Further customization on the quality of the dithering and some optimizations around
not repeating dithering on images.

© 2024 Franklin Maloney , released as AGPLv3
# see https://www.gnu.org/licenses/agpl-3.0.html
"""


from PIL import Image
import dithering
import shutil
import logging
import argparse
import os

parser = argpasrse.ArgumentParser(
    """
    Traverses folders and dithers/colorizes images based on
    the folder that they are contained in. Will only dither images that are not
    already in the dithered folder.
    """
)

parser.add_argument(
    '-d', '--directory', help='set the directory', default = '.'
)


parser.add_argument(
    '-c', '--colorize', help='specifies whether to colorize the images', action='store_true'
)


args = parser.parse_args()

image_ext = [".jpg", ".JPG", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp"]
