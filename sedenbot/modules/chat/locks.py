# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from pyrogram.types import ChatPermissions
from sedenbot import HELP
from sedenecem.core import edit, get_translation, parse_cmd, sedenify


@sedenify(pattern='^.(un|)lock', private=False, admin=True)
def lock_unlock_chat(message):
    text = (message.text or message.caption).replace(r'\s+', ' ').split(' ', 1)

    unlock = parse_cmd(text[0])[:2] == 'un'
    if len(text) < 2:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return

    args = text[1].lower()

    msg = None
    media = None
    other = None
    webprev = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if args == 'msg':
        msg = unlock
        usage = get_translation('lockMsg')
    elif args == 'media':
        media = unlock
        usage = get_translation('lockMedia')
    elif args == 'other':
        other = unlock
        usage = get_translation('lockOther')
    elif args == 'web':
        webprev = unlock
        usage = get_translation('lockWeb')
    elif args == 'poll':
        gpoll = unlock
        usage = get_translation('lockPoll')
    elif args == 'invite':
        adduser = unlock
        usage = get_translation('lockInvite')
    elif args == 'pin':
        cpin = unlock
        usage = get_translation('lockPin')
    elif args == 'info':
        changeinfo = unlock
        usage = get_translation('lockInformation')
    elif args == 'all':
        msg = unlock
        media = unlock
        other = unlock
        webprev = unlock
        gpoll = unlock
        adduser = unlock
        cpin = unlock
        changeinfo = unlock
        usage = get_translation('lockAll')
    else:
        if not args:
            edit(
                message,
                get_translation('locksUnlockNoArgs' if usage else 'locksLockNoArgs'),
            )
            return
        else:
            edit(message, get_translation('lockError', ['`', args]))
            return

    chat = message._client.get_chat(message.chat.id)

    msg = get_on_none(msg, chat.permissions.can_send_messages)
    media = get_on_none(media, chat.permissions.can_send_media_messages)
    other = get_on_none(other, chat.permissions.can_send_other_messages)
    webprev = get_on_none(webprev, chat.permissions.can_add_web_page_previews)
    gpoll = get_on_none(gpoll, chat.permissions.can_send_polls)
    adduser = get_on_none(adduser, chat.permissions.can_invite_users)
    cpin = get_on_none(cpin, chat.permissions.can_pin_messages)
    changeinfo = get_on_none(changeinfo, chat.permissions.can_change_info)

    try:
        message._client.set_chat_permissions(
            message.chat.id,
            ChatPermissions(
                can_send_messages=msg,
                can_send_media_messages=media,
                can_send_other_messages=other,
                can_add_web_page_previews=webprev,
                can_send_polls=gpoll,
                can_change_info=changeinfo,
                can_invite_users=adduser,
                can_pin_messages=cpin,
            ),
        )
        edit(
            message,
            get_translation(
                'locksUnlockSuccess' if unlock else 'locksLockSuccess', ['`', usage]
            ),
        )
    except BaseException as e:
        edit(message, get_translation('lockPerm', ['`', '**', str(e)]))
        return


def get_on_none(item, defval):
    if item is None:
        return defval

    return item


HELP.update({'locks': get_translation('lockInfo')})
