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
from sedenecem.core import sedenify, reply

# Copyright (c) @NaytSeyd | 2020


@sedenify(pattern='^.tagall$', compat=False, private=False)
def tagall(client, message):
    mesaj = '@tag'
    chat = message.chat
    uzunluk = 0
    for member in client.iter_chat_members(chat.id):
        if uzunluk < 4092:
            mesaj += f'[\u2063](tg://user?id={member.user.id})'
            uzunluk += 1
    reply(message, mesaj, fix_markdown=True)
    message.delete()


@sedenify(pattern='^.admin$', compat=False, private=False)
def admin(client, message):
    mesaj = '@admin'
    chat = message.chat
    for member in client.iter_chat_members(chat.id, filter='administrators'):
        mesaj += f'[\u2063](tg://user?id={member.user.id})'
    yanit = message.reply_to_message
    reply(yanit if yanit else message, mesaj, fix_markdown=True)
    message.delete()


KOMUT.update({
    "tagall":
    ".tagall\
    \nKullanım: Bu komutu kullandığınızda sohbet içerisinde ki herkesi etiketler.\n\n.admin \
    \nKullanım: Bu komutu kullandığınızda sohbet içerisinde ki yöneticileri etiketler."
})
