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
from sedenecem.core import edit, extract_args, sedenify

@sedenify(pattern=r'^.(un)?lock', compat=False, private=False)
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
        kullanim = "mesaj atma"
    elif kilit == "media":
        media = unlock
        kullanim = "medya yollama"
    elif kilit == "gif":
        gif = unlock
        sticker = gif
        kullanim = "GIF ve çıkartma yollama"
    elif kilit == "game":
        gamee = unlock
        kullanim = "oyun"
    elif kilit == "inline":
        ainline = unlock
        kullanim = "sohbet içi botlar"
    elif kilit == "web":
        webprev = unlock
        kullanim = "web sayfa önizlemesi"
    elif kilit == "poll":
        gpoll = unlock
        kullanim = "anket yollama"
    elif kilit == "invite":
        adduser = unlock
        kullanim = "davet etme"
    elif kilit == "pin":
        cpin = unlock
        kullanim = "sabitleme"
    elif kilit == "info":
        changeinfo = unlock
        kullanim = "sohbet bilgisi değiştirme"
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
        kullanim = "her şey"
    else:
        if not kilit:
            edit(message, f'`Hiçliği{"n kilidini açamam" if unlock else " kilitleyemem"} dostum!`')
            return
        else:
            edit(message, f'`Geçersiz medya tipi:` {kilit}')
            return

    kilitle = client.get_chat(message.chat.id)

    msg = get_on_none(msg, kilitle.permissions.can_send_messages)
    media = get_on_none(media, kilitle.permissions.can_send_media_messages)
    sticker = get_on_none(sticker, kilitle.permissions.can_send_stickers)
    gif = get_on_none(gif, kilitle.permissions.can_send_animations)
    gamee = get_on_none(gamee, kilitle.permissions.can_send_games)
    ainline = get_on_none(ainline, kilitle.permissions.can_use_inline_bots)
    webprev = get_on_none(webprev, kilitle.permissions.can_add_web_page_previews)
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
        edit(message, f'`Bu sohbet için {kullanim} {"kilidi açıldı" if unlock else "kilitlendi"}!`')
    except BaseException as e:
        edit(message, f'`Bunun için gerekli haklara sahip olduğuna emin misin?`\n**Hata:** {str(e)}')
        return


def get_on_none(item, defval):
    if item == None:
        return defval

    return item


KOMUT.update({
    "locks":
    ".lock <kilitlenecek medya tipi> veya .unlock <kilitlenecek medya tipi>\
\nKullanım: Sohbetteki birtakım şeyleri engelleyebilmeni sağlar. (sticker atmak, oyun oynamak vs.)\
[Not: Yönetici hakları gerektirir!]\
\n\nKilitleyebileceğin ve kilidini açabileceklerin şunlardır: \
\n`all, msg, media, sticker, gif, game, inline, web, poll, invite, pin, info`"
})
