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
from sedenecem.core import edit, sedenify, send_log, get_translation


@sedenify(pattern='.chatid$', private=False)
def chatid(message):
    edit(
        message,
        f"{get_translation('chatidInfo', ['`', str(message.chat.id)])}")


@sedenify(pattern='^.kickme$', compat=False, private=False)
def kickme(client, message):
    edit(message, f'`{get_translation("kickmeInfo")}`')
    client.leave_chat(message.chat.id, 'me')


@sedenify(pattern='^.unmutechat$')
def unmutechat(message):
    try:
        from sedenecem.sql.keep_read_sql import unkread
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    status = unkread(str(message.chat.id))
    if status:
        edit(message, f'`{get_translation("chatUnmuted")}`')
    else:
        edit(message, f'`{get_translation("chatAlreadyUnmuted")}`')
    sleep(2)
    message.delete()


@sedenify(pattern='^.mutechat$')
def mutechat(message):
    try:
        from sedenecem.sql.keep_read_sql import kread
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    status = kread(str(message.chat.id))
    if status:
        edit(message, f'`{get_translation("chatMuted")}`')
    else:
        edit(message, f'`{get_translation("chatAlreadyMuted")}`')
    sleep(2)
    message.delete()

    send_log(get_translation("chatLog", [message.chat.id]))


@sedenify(incoming=True, compat=False)
def keep_read(client, message):
    if message.from_user and message.from_user.is_self:
        message.continue_propagation()

    try:
        from sedenecem.sql.keep_read_sql import is_kread
    except BaseException:
        return

    if is_muted(message.chat.id):
        client.read_history(message.chat.id)

    message.continue_propagation()


def is_muted(chat_id):
    try:
        from sedenecem.sql.keep_read_sql import is_kread
    except BaseException:
        return False

    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(chat_id):
                return True

    return False


KOMUT.update({"chat": get_translation('infoChatID')})
