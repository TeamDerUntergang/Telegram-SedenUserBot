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

from pyrogram import ChatPermissions

from sedenbot import KOMUT
from sedenecem.core import edit, extract_args, sedenify, get_translation


@sedenify(pattern=r'^.(un|)lock', compat=False, private=False)
def lock(client, message):
    text = message.text
    unlock = text[1:3] == 'un'
    kilit = ''
    if ' ' in text:
        kilit = extract_args(message).lower()
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    webprev = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if kilit == "msg":
        msg = unlock
        kullanim = f'{get_translation("lockMsg")}'
    elif kilit == "media":
        media = unlock
        kullanim = f'{get_translation("lockMedia")}'
    elif kilit == "gif":
        gif = unlock
        sticker = gif
        kullanim = f'{get_translation("lockGif")}'
    elif kilit == "game":
        gamee = unlock
        kullanim = f'{get_translation("lockGame")}'
    elif kilit == "inline":
        ainline = unlock
        kullanim = f'{get_translation("lockInline")}'
    elif kilit == "web":
        webprev = unlock
        kullanim = f'{get_translation("lockWeb")}'
    elif kilit == "poll":
        gpoll = unlock
        kullanim = f'{get_translation("lockPoll")}'
    elif kilit == "invite":
        adduser = unlock
        kullanim = f'{get_translation("lockInvite")}'
    elif kilit == "pin":
        cpin = unlock
        kullanim = f'{get_translation("lockPin")}'
    elif kilit == "info":
        changeinfo = unlock
        kullanim = f'{get_translation("lockInformation")}'
    elif kilit == "all":
        msg = unlock
        media = unlock
        gif = unlock
        gamee = unlock
        ainline = unlock
        webprev = unlock
        gpoll = unlock
        adduser = unlock
        cpin = unlock
        changeinfo = unlock
        kullanim = f'{get_translation("lockAll")}'
    else:
        if not kilit:
            edit(
                message,
                f"{get_translation('locksUnlockNoArgs' if unlock else 'locksLockNoArgs')}")
            return
        else:
            edit(message, get_translation("lockError", ['`', kilit]))
            return

    kilitle = client.get_chat(message.chat.id)

    msg = get_on_none(msg, kilitle.permissions.can_send_messages)
    media = get_on_none(media, kilitle.permissions.can_send_media_messages)
    sticker = get_on_none(sticker, kilitle.permissions.can_send_stickers)
    gif = get_on_none(gif, kilitle.permissions.can_send_animations)
    gamee = get_on_none(gamee, kilitle.permissions.can_send_games)
    ainline = get_on_none(ainline, kilitle.permissions.can_use_inline_bots)
    webprev = get_on_none(
        webprev, kilitle.permissions.can_add_web_page_previews)
    gpoll = get_on_none(gpoll, kilitle.permissions.can_send_polls)
    adduser = get_on_none(adduser, kilitle.permissions.can_invite_users)
    cpin = get_on_none(cpin, kilitle.permissions.can_pin_messages)
    changeinfo = get_on_none(changeinfo, kilitle.permissions.can_change_info)

    try:
        client.set_chat_permissions(message.chat.id, ChatPermissions(
            can_send_messages=msg,
            can_send_media_messages=media,
            can_send_stickers=sticker,
            can_send_animations=gif,
            can_send_games=gamee,
            can_use_inline_bots=ainline,
            can_add_web_page_previews=webprev,
            can_send_polls=gpoll,
            can_change_info=changeinfo,
            can_invite_users=adduser,
            can_pin_messages=cpin
        ))
        edit(
            message, get_translation(
                'locksUnlockSuccess' if unlock else 'locksLockSuccess', [
                    '`', kullanim]))
    except BaseException as e:
        edit(message, get_translation("lockPerm", ['`', '**', str(e)]))
        return


def get_on_none(item, defval):
    if item is None:
        return defval

    return item


KOMUT.update({"locks": get_translation("lockInfo")})
