# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from pyrogram import enums
from sedenbot import BRAIN, HELP, SPAMWATCH_KEY
from sedenecem.core import get_translation, is_admin_myself, reply, sedenify, send_log

from spamwatch import Client as SpamWatch


class SWClient:
    spamwatch_client = SpamWatch(SPAMWATCH_KEY) if SPAMWATCH_KEY else None


@sedenify(
    outgoing=False,
    incoming=True,
    disable_edited=True,
    disable_notify=True,
)
def spamwatch_action(message):
    if not SWClient.spamwatch_client:
        message.continue_propagation()

    uid = message.from_user.id
    if uid in BRAIN:
        message.continue_propagation()

    ban_status = SWClient.spamwatch_client.get_ban(uid)
    if not ban_status:
        message.continue_propagation()

    if is_admin_myself(message.chat):
        text = get_translation('spamWatchBan', [message.from_user.first_name, uid])

        if message.chat.type == enums.ChatType.PRIVATE:
            reply(message, text)
            message._client.block_user(uid)
        else:
            myself = message.chat.get_member('me')
            if myself.privileges and myself.privileges.can_restrict_members:
                message.chat.ban_member(uid)
                reply(message, text)
            else:
                return

        send_log(text)


HELP.update({'spamwatch': get_translation('spamWatchInfo')})
