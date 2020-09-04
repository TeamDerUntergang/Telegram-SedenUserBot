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

from pyrogram.errors import YouBlockedUser

from sedenbot import KOMUT
from sedenecem.conv import PyroConversation
from sedenecem.core import sedenify, edit

@sedenify(pattern='^.sangmata$', compat=False)
def sangmata(client, message):
    reply = message.reply_to_message
    if reply and reply.text:
        edit(message, '`İşleniyor...`')
    else:
        edit(message, '`Bir mesaja yanıt verin.`')
        return

    chat = 'SangMataInfo_bot'

    with PyroConversation(client, chat) as conv:
        response = None
        try:
            msg = conv.forward_msg(reply)
            response = conv.recv_msg()
        except YouBlockedUser:
            edit(message, f'`Lütfen` **@{chat}** `engelini kaldırın ve tekrar deneyin`')
            return
        except Exception as e:
            raise e

        if not response:
            edit(message, '`Botdan cevap alamadım!`')
        elif response.text and response.text.startswith('Forward'):
            edit(message, '`Gizlilik ayarları bunu yapmama engel oldu.`')
        else:
            edit(message, response.text)

KOMUT.update({
    "sangmata":
    ".sangmata \
    \nKullanım: Belirtilen kullanıcının isim geçmişini görüntüleyin.\n"
})
