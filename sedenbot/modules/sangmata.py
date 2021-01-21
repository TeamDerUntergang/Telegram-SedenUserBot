# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from pyrogram.errors import YouBlockedUser

from sedenbot import HELP
from sedenecem.core import sedenify, edit, get_translation, PyroConversation


@sedenify(pattern='^.sangmata$', compat=False)
def sangmata(client, message):
    reply = message.reply_to_message
    if reply and reply.text:
        edit(message, f'`{get_translation("processing")}`')
    else:
        edit(message, f'`{get_translation("replyMessage")}`')
        return

    chat = 'SangMataInfo_bot'

    with PyroConversation(client, chat) as conv:
        response = None
        try:
            conv.forward_msg(reply)
            response = conv.recv_msg()
        except YouBlockedUser:
            edit(message, get_translation('unblockChat', ['**', '`', chat]))
            return
        except Exception as e:
            raise e

        if not response:
            edit(message, f'`{get_translation("answerFromBot")}`')
        elif response.text and response.text.startswith('Forward'):
            edit(message, f'`{get_translation("privacySettings")}`')
        else:
            edit(message, response.text)


HELP.update({'sangmata': get_translation('sangmataInfo')})
