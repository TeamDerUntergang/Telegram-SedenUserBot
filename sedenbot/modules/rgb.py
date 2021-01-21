# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from io import BytesIO
from os import remove
from random import randint
from textwrap import wrap

from PIL import Image, ImageChops, ImageDraw, ImageFont

from sedenbot import HELP
from sedenecem.core import (extract_args, sedenify, edit,
                            send_sticker, get_translation)


@sedenify(pattern='^.rgb', compat=False)
def sticklet(client, message):
    R = randint(0, 256)
    G = randint(0, 256)
    B = randint(0, 256)

    sticktext = extract_args(message)

    if len(sticktext) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    edit(message, f'`{get_translation("rgbProcessing")}`')

    # https://docs.python.org/3/library/textwrap.html#textwrap.wrap
    sticktext = wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new('RGBA', (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = 'sedenecem/fonts/GoogleSans.ttf'

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    step = 1
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 10 * step
        step += 1.5
        font = ImageFont.truetype(FONT_FILE, size=int(fontsize))

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512 - width) / 2, (512 - height) / 2),
                        sticktext, font=font, fill=(R, G, B))

    image_stream = BytesIO()
    image_stream.name = 'image.webp'

    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        return im.crop(bbox) if bbox else im

    image = trim(image)
    image.save(image_stream, 'WebP')
    image_stream.seek(0)

    send_sticker(client, message.chat, image_stream)
    message.delete()
    try:
        remove(image_stream.name)
    except BaseException:
        pass


HELP.update({'rgb': get_translation('rgbInfo')})
