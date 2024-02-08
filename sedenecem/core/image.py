# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from math import floor

from PIL import Image

from .misc import get_download_dir, get_status_out


def sticker_resize(photo):
    """
    Resizes a given sticker image file to have a maximum dimension of 512 pixels while maintaining aspect ratio.
    If the image is already smaller than 512x512 pixels, it will be resized to its original size.

    Args:
        photo (str): The file path to the sticker image file to be resized.

    Returns:
        str: The file path to the resized image file in PNG format, stored in a temporary directory.
    """
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = floor(size1new)
        size2new = floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)

    temp = f'{get_download_dir()}/temp.png'
    image.save(temp, 'PNG')
    return temp


def video_convert(video):
    """
    Converts a video file to a webm format with dimensions of 512x512 and duration of 3.0 seconds.

    Args:
        video (str): Path of the video file to be converted.

    Returns:
        str: Path of the converted webm file.
    """
    get_status_out(
        f'ffmpeg -i {video} \
        -vf scale=512:512:force_original_aspect_ratio=decrease \
        -c:v libvpx-vp9 \
        -crf 30 \
        -b:v 500k \
        -pix_fmt yuv420p \
        -t 2.9 \
        -an \
        -y {get_download_dir()}/temp.webm'
    )
    output = f'{get_download_dir()}/temp.webm'
    return output
