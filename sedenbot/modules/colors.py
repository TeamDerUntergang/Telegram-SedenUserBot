# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from PIL import Image, ImageColor

from sedenbot import KOMUT
from sedenecem.core import (edit, reply_img, extract_args,
                            sedenify, get_translation)


@sedenify(pattern='^.color')
def color(message):
    input_str = extract_args(message)
    reply = message.reply_to_message
    message_id = message.chat.id
    if reply:
        message_id
    if input_str.startswith('#'):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            edit(message, str(e))
            return False
        else:
            im = Image.new(mode='RGB', size=(1920, 1080), color=usercolor)
            im.save('sedencik.png', 'PNG')
            input_str = input_str.replace('#', '#RENK_')
            reply_img(message, 'sedencik.png',
                      caption=input_str, delete_file=True)
            message.delete()
    else:
        edit(message, f'`{get_translation("colorsUsage")}`')


KOMUT.update({'color': get_translation('colorsInfo')})
