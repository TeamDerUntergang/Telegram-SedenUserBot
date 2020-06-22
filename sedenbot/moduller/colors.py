# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# @NaytSeyd tarafından portlanmıştır
#

import os
from PIL import Image, ImageColor

from sedenbot import KOMUT
from sedenecem.events import edit, reply_img, extract_args, sedenify

@sedenify(pattern='^.color')
def color(message):
    input_str = extract_args(message)
    message_id = message.chat.id
    if message.reply_to_message:
        message_id = message.reply_to_message
    if input_str.startswith('#'):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            edit(message, str(e))
            return False
        else:
            im = Image.new(mode='RGB', size=(1280, 720), color=usercolor)
            im.save('sedencik.png', 'PNG')
            input_str = input_str.replace('#', '#RENK_')
            reply_img(message, 'sedencik.png', caption=input_str)
            os.remove('sedencik.png')
            message.delete()
    else:
        edit(message, "Belki burayı okuyarak bir şeyler öğrenebilirsin.. \
                      `.color <renk kodu>  | Örnek: .color #330066`")

KOMUT.update({
    'color': ".color <renk kodu> \
\nKullanım: Belirttiğniz renk kodunun çıktısını alın. \
\nÖrnek: .color #330066"
})
