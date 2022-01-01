# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove
from random import randint, uniform

from PIL import Image, ImageEnhance, ImageOps
from sedenbot import HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    get_translation,
    parse_cmd,
    reply_img,
    sedenify,
)


@sedenify(pattern='^.(deepf|f)ry')
def deepfry(message):

    text = (message.text or message.caption).split(' ', 1)
    fry = parse_cmd(text[0]) == 'fry'

    try:
        frycount = int(text[1])
        if frycount < 1:
            raise ValueError
    except BaseException:
        frycount = 1

    MAX_LIMIT = 5
    if frycount > MAX_LIMIT:
        frycount = MAX_LIMIT

    reply = message.reply_to_message

    if not reply and message.caption:
        reply = message

    if reply:
        data = check_media(reply)

        if not data:
            edit(message, f'`{get_translation("deepfryError")}`')
            return
    else:
        edit(
            message,
            get_translation('deepfryNoPic', ['`', f'{"f" if fry else "deepf"}ry']),
        )
        return

    # Download Media
    edit(message, f'`{get_translation("deepfryDownload")}`')
    image_file = download_media_wc(reply, 'image.png')
    image = Image.open(image_file)
    remove(image_file)

    # Apply effect to media
    edit(message, get_translation('deepfryApply', ['`', f'{"" if fry else "deep"}']))
    for _ in range(frycount):
        image = deepfry_media(image, fry)

    fried_io = open('image.jpeg', 'w+')
    image.save(fried_io, 'JPEG')
    fried_io.close()

    reply_img(reply or message, 'image.jpeg', delete_file=True)
    message.delete()


def deepfry_media(img: Image, fry: bool) -> Image:
    colors = None
    if fry:
        colors = (
            (randint(50, 200), randint(40, 170), randint(40, 190)),
            (randint(190, 255), randint(170, 240), randint(180, 250)),
        )

    # Set image format
    img = img.copy().convert('RGB')
    width, height = img.width, img.height

    temp_num = uniform(0.8, 0.9) if fry else 0.75
    img = img.resize(
        (int(width ** temp_num), int(height ** temp_num)), resample=Image.LANCZOS
    )

    temp_num = uniform(0.85, 0.95) if fry else 0.88
    img = img.resize(
        (int(width ** temp_num), int(height ** temp_num)), resample=Image.BILINEAR
    )

    temp_num = uniform(0.89, 0.98) if fry else 0.9
    img = img.resize(
        (int(width ** temp_num), int(height ** temp_num)), resample=Image.BICUBIC
    )
    img = img.resize((width, height), resample=Image.BICUBIC)

    temp_num = randint(3, 7) if fry else 4
    img = ImageOps.posterize(img, temp_num)

    # Create a color scheme
    overlay = img.split()[0]

    temp_num = uniform(1.0, 2.0) if fry else 2
    overlay = ImageEnhance.Contrast(overlay).enhance(temp_num)

    temp_num = uniform(1.0, 2.0) if fry else 1.5
    overlay = ImageEnhance.Brightness(overlay).enhance(temp_num)

    overlay = ImageOps.colorize(
        overlay, colors[0] if fry else (254, 0, 2), colors[1] if fry else (255, 255, 15)
    )

    # Place red and yellow in image and sharpen
    temp_num = uniform(0.1, 0.4) if fry else 0.75
    img = Image.blend(img, overlay, temp_num)

    temp_num = randint(5, 300) if fry else 100
    img = ImageEnhance.Sharpness(img).enhance(temp_num)

    return img


def check_media(reply_message):
    data = False

    if reply_message and reply_message.media:
        if reply_message.photo:
            data = True
        elif reply_message.sticker and not reply_message.sticker.is_animated:
            data = True
        elif reply_message.document:
            name = reply_message.document.file_name
            if (
                name
                and '.' in name
                and name[name.find('.') + 1 :] in ['png', 'jpg', 'jpeg', 'webp']
            ):
                data = True

    return data


HELP.update({'deepfry': get_translation('deepfryInfo')})
