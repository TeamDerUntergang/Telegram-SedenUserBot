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

from time import sleep
from sedenbot import KOMUT
from sedenecem.conv import PyroConversation
from sedenecem.core import sedenify, edit

@sedenify(pattern='^.q$', compat=False)
def quotly(client, message):
    reply = message.reply_to_message
    if reply and (reply.text or reply.photo or reply.sticker):
        edit(message, '`Alıntı yapılıyor ...`')
    else:
        edit(message, '`Bir mesaja yanıt verin.`')
        return
    
    sleep(1)
    chat = 'QuotLyBot'

    with PyroConversation(client, chat) as conv:
        response = None
        try:
            msg = conv.forward_msg(reply)
            response = conv.recv_msg()
        except: # pylint: disable=W0702
            edit(message, '`Bottan yanıt alamadım. Muhtemelen bu gruba ekli veya botu engelledin.`')
            return

        if response.text and response.text.startswith('Forward'):
            edit(message, '`Gizlilik ayarları bunu yapmama engel oldu.`')
            return

        response.forward(message.chat.id, as_copy=True)

    message.delete()

KOMUT.update({
    "quotly":
    ".q \
    \nKullanım: Metninizi çıkartmaya dönüştürün.\n"
})
