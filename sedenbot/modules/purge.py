# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep

from pyrogram.errors import FloodWait
from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    reply,
    sedenify,
    send_log,
)


@sedenify(pattern='^.purge$', compat=False, admin=True)
def purge(client, message):
    msg = message.reply_to_message
    if msg:
        itermsg = client.iter_history(
            message.chat.id, offset_id=msg.message_id, reverse=True
        )
    else:
        edit(message, f'`{get_translation("purgeUsage")}`')
        return

    count = 0

    for message in itermsg:
        try:
            count = count + 1
            client.delete_messages(message.chat.id, message.message_id)
        except FloodWait as e:
            sleep(e.x)
        except Exception as e:
            edit(message, get_translation('purgeError', ['`', '**', e]))
            return

    done = reply(message, get_translation('purgeResult', ['**', '`', str(count)]))
    send_log(get_translation('purgeLog', ['**', '`', str(count)]))
    sleep(2)
    done.delete()


@sedenify(pattern='^.purgeme', compat=False)
def purgeme(client, message):
    count = extract_args(message)
    if not count.isdigit():
        return edit(message, f'`{get_translation("purgemeUsage")}`')
    i = 1

    itermsg = client.get_history(message.chat.id)
    for message in itermsg:
        if i > int(count) + 1:
            break
        i = i + 1
        message.delete()

    smsg = reply(message, get_translation('purgeResult', ['**', '`', str(count)]))
    send_log(get_translation('purgeLog', ['**', '`', str(count)]))
    sleep(2)
    i = 1
    smsg.delete()


@sedenify(pattern='^.del$', compat=False, admin=True)
def delete(client, message):
    msg_src = message.reply_to_message
    if msg_src:
        if msg_src.from_user.id:
            try:
                client.delete_messages(message.chat.id, msg_src.message_id)
                message.delete()
                send_log(f'`{get_translation("delResultLog")}`')
            except BaseException:
                send_log(f'`{get_translation("delErrorLog")}`')
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')


HELP.update({'purge': get_translation('purgeInfo')})
HELP.update({'purgeme': get_translation('purgemeInfo')})
HELP.update({'del': get_translation('delInfo')})
