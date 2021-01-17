# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from sedenbot import HELP
from sedenecem.core import sedenify, reply, get_translation


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


HELP.update({'tagall': get_translation('tagallInfo')})
