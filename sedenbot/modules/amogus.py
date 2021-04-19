# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from io import BytesIO
from random import randint
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont
from requests import get
from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, sedenify, send_sticker


@sedenify(pattern='^.(amogu|su)s', compat=False)
def amogus(client, message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    edit(message, f"`{get_translation('processing')}`")

    arr = randint(1, 12)
    fontsize = 100
    FONT_FILE = 'sedenecem/fonts/OpenSans.ttf'
    url = 'https://raw.githubusercontent.com/KeyZenD/AmongUs/master/'  # Thanks
    font = ImageFont.truetype(FONT_FILE, size=int(fontsize))

    imposter = Image.open(BytesIO(get(f'{url}{arr}.png').content))
    text_ = '\n'.join(['\n'.join(wrap(part, 30)) for part in args.split('\n')])
    w, h = ImageDraw.Draw(Image.new('RGB', (1, 1))).multiline_textsize(
        text_, font, stroke_width=2
    )
    text = Image.new('RGBA', (w + 40, h + 40))
    ImageDraw.Draw(text).multiline_text(
        (15, 15), text_, '#FFF', font, stroke_width=2, stroke_fill='#000'
    )
    w = imposter.width + text.width + 30
    h = max(imposter.height, text.height)
    image = Image.new('RGBA', (w, h))
    image.paste(imposter, (0, h - imposter.height), imposter)
    image.paste(text, (w - text.width, 0), text)
    image.thumbnail((512, 512))

    output = BytesIO()
    output.name = 'sus.webp'
    image.save(output, 'WebP')
    output.seek(0)

    send_sticker(client, message.chat, output)
    message.delete()


HELP.update({'amogus': get_translation('amogusInfo')})