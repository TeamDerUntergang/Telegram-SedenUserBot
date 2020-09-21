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

from sedenbot import KOMUT, LOG_ID
from sedenecem.core import extract_args, sedenify, edit, get_messages, reply_msg, forward, send_log, get_translation


@sedenify(pattern='^.addsnip')
def save_snip(message):
    try:
        from sedenecem.sql.snips_sql import add_snip
    except AttributeError:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    args = extract_args(message, markdown=True).split(' ', 1)
    if len(args) < 1 or len(args[0]) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    keyword = args[0]
    string = args[1] if len(args) > 1 else ''
    msg = message.reply_to_message
    msg_id = None

    if len(string) < 1:
        if msg:
            if msg.text:
                string = msg.text.markdown
            else:
                string = None
                msg_o = forward(msg, LOG_ID)
                if not msg_o:
                    edit(
                        message, f'`{get_translation("snipError")}`')
                    return
                msg_id = msg_o.message_id
                send_log(get_translation(
                    'snipsLog', [message.chat.id, keyword]))
        else:
            edit(message, f'`{get_translation("wrongCommand")}`')

    if add_snip(keyword, string, msg_id) is False:
        edit(message, get_translation('snipsUpdated', ['`', keyword]))
    else:
        edit(message, get_translation('snipsAdded', ['`', keyword]))


@sedenify(pattern='^.snips$')
def snip_list(message):
    try:
        from sedenecem.sql.snips_sql import get_snips
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    list = f'`{get_translation("noSnip")}`'
    all_snips = get_snips()
    for a_snip in all_snips:
        if list == f'`{get_translation("noSnip")}`':
            list = f'{get_translation("snipChats")}\n'
            list += f'`${a_snip.snip}`\n'
        else:
            list += f'`${a_snip.snip}`\n'

    edit(message, list)


@sedenify(pattern='^.remsnip')
def delete_snip(message):
    try:
        from sedenecem.sql.snips_sql import remove_snip
    except AttributeError:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    name = extract_args(message)
    if len(name) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    if remove_snip(name) is False:
        edit(message, get_translation('snipsNotFound', ['`', name]))
    else:
        edit(message, get_translation('snipsRemoved', ['**', '`', name]))


def get_snip(message):
    try:
        try:
            from sedenecem.sql.snips_sql import get_snip
        except BaseException:
            edit(message, f'`{get_translation("nonSqlMode")}`')
            return

        snipname = extract_args(message).split()[0][1:]
        snip = get_snip(snipname)

        if snip:
            if snip.f_mesg_id:
                msg_o = get_messages(LOG_ID, msg_ids=int(snip.f_mesg_id))
                if msg_o and len(msg_o) > 0 and not msg_o[-1].empty:
                    msg = msg_o[-1]
                    reply_msg(message, msg)
                else:
                    edit(message, f'`{get_translation("snipResult")}`')
            elif snip.reply and len(snip.reply) > 0:
                edit(message, snip.reply)
            else:
                edit(message, f'`{get_translation("snipError2")}`')
        else:
            edit(message, f'`{get_translation("snipNotFound")}`')
    except BaseException:
        pass


KOMUT.update({"snips": get_translation("snipInfo")})
