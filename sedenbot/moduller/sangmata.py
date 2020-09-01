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

from sedenbot import KOMUT
from sedenecem.conv import PyroConversation
from sedenecem.core import sedenify, edit

@sedenify(pattern='^.sangmata$', compat=False)
def sangmata(client, message):
    reply = message.reply_to_message
    if not reply or not reply.text:
        edit(message, '`Bir mesaja yanıt verin.`')
        return

    chat = 'SangMataInfo_bot'
    edit(message, '`İşleniyor ...`')

    with PyroConversation(client, chat) as conv:
        response = None
        try:
            msg = conv.forward_msg(reply)
            response = conv.recv_msg()
        except: # pylint: disable=W0702
            edit(message, '`Bottan yanıt alamadım. Muhtemelen botu engelledin.`')
            return

        if response.text and response.text.startswith('Forward'):
            edit(message, '`Gizlilik ayarları bunu yapmama engel oldu.`')
            return

        response.forward(message.chat.id, as_copy=True)

    message.delete()


KOMUT.update({
    "sangmata":
    ".sangmata \
    \nKullanım: Belirtilen kullanıcının isim geçmişini görüntüleyin.\n"
})
