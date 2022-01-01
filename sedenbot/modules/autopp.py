# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from datetime import datetime
from os import path, remove
from time import sleep

from PIL import Image, ImageDraw, ImageFont
from requests import get
from sedenbot import AUTO_PP, HELP, LOGS, TEMP_SETTINGS
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_translation,
    sedenify,
)

# =================== CONSTANT ===================
KEY_AUTOPP = 'autopic'
# ================================================


@sedenify(pattern='^.autopp', compat=False)
def autopic(client, message):
    args = extract_args(message)
    autopic = KEY_AUTOPP in TEMP_SETTINGS
    if args == 'disable':
        if autopic:
            del TEMP_SETTINGS[KEY_AUTOPP]
            edit(message, f'`{get_translation("autoppDisabled")}`')
            return
        else:
            edit(message, f'`{get_translation("autoppDisabledAlready")}`')
            return
    elif autopic:
        edit(message, f'`{get_translation("autoppEnabledAlready")}`')
        return

    TEMP_SETTINGS[KEY_AUTOPP] = True

    edit(message, f'`{get_translation("autoppProcess")}`')

    FONT_FILE = 'sedenecem/fonts/GoogleSans.ttf'

    downloaded_file_name = 'oldpp.png'
    photo = 'newpp.png'

    if path.exists(downloaded_file_name):
        LOGS.info(get_translation('autoppLog'))
    else:
        if AUTO_PP and len(AUTO_PP) > 0:
            with open(downloaded_file_name, 'wb') as load:
                load.write(get(AUTO_PP).content)
        else:
            try:
                profile_photo = client.get_profile_photos('me', limit=1)
                downloaded_file_name = download_media_wc(
                    profile_photo[0], downloaded_file_name
                )
            except BaseException:
                edit(message, f'`{get_translation("autoppConfig")}`')
                return

    edit(message, f'`{get_translation("autoppResult")}`')

    while KEY_AUTOPP in TEMP_SETTINGS:
        try:
            current_time = datetime.now().strftime('%H:%M')
            img = Image.open(downloaded_file_name)
            drawn_text = ImageDraw.Draw(img)
            fnt = ImageFont.truetype(FONT_FILE, 70)
            size = drawn_text.multiline_textsize(current_time, font=fnt)
            drawn_text.text(
                ((img.width - size[0]) / 2, (img.height - size[1])),
                current_time,
                font=fnt,
                fill=(255, 255, 255),
            )
            img.save(photo)
            client.set_profile_photo(photo=photo)
            remove(photo)
            sleep(60)
        except BaseException:
            return


HELP.update({'autopp': get_translation('autoppInfo')})
