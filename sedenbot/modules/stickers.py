# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from random import choice
from requests import get

from pyrogram.api.functions.messages import GetStickerSet
from pyrogram.api.types import InputStickerSetShortName

from sedenbot import KOMUT, me
from sedenecem.core import (
    edit,
    sedenify,
    download_media,
    download_media_wc,
    reply_doc,
    get_translation,
    extract_args,
    PyroConversation,
    sticker_resize as resizer)
# ================= CONSTANT =================
DIZCILIK = [get_translation(f'kangstr{i+1}') for i in range(0, 12)]
# ================= CONSTANT =================


@sedenify(pattern='^.(d[ıi]zla|kang|world)', compat=False)
def kang(client, message):
    myacc = me[0]
    kanger = myacc.username or myacc.first_name
    if myacc.username:
        kanger = f'@{kanger}'
    args = extract_args(message)

    reply = message.reply_to_message
    if not reply:
        edit(message, f'`{get_translation("stickerUsage")}`')
        return

    anim = False
    media = None

    if(reply.photo or reply.document or reply.sticker):
        edit(message, f'`{choice(DIZCILIK)}`')
        anim = reply.sticker and reply.sticker.is_animated
        media = download_media(client, reply, sticker_orig=anim)
    else:
        edit(message, f'`{get_translation("stickerError")}`')
        return

    if len(args) < 1:
        args = 1

    emoji = '🤤'

    if ' ' in str(args):
        emoji, args = args.split(' ', 1)

    pack = 1 if not str(args).isdigit() else int(args)

    pname = f'trzworld{pack}'
    pnick = f"trz's world {pack}"

    limit = '50' if anim else '120'

    def pack_created():
        created = get(f'https://telegram.me/addstickers/{pname}')
        created = (('A <strong>Telegram</strong> user has created the '
                    '<strong>Sticker&nbsp;Set</strong>') not in created.text)
        return created

    def create_new(conv, pack):
        cmd = f'/new{"animated" if anim else "pack"}'

        try:
            send_recv(conv, cmd)
        except Exception as e:
            raise e
        msg = send_recv(conv, pnick)
        if msg.text == 'Invalid pack selected.':
            pack += 1
            return create_new(conv)
        msg = send_recv(conv, media, doc=True)
        if 'Sorry, the file type is invalid.' in msg.text:
            edit(message, f'`{get_translation("stickerError")}`')
            return
        send_recv(conv, emoji)
        send_recv(conv, '/publish')
        if anim:
            send_recv(conv, f'<{pnick}>')
        send_recv(conv, '/skip')
        send_recv(conv, pname)

    def add_exist(conv, pack, pname, pnick):
        try:
            send_recv(conv, '/addsticker')
        except Exception as e:
            raise e

        status = send_recv(conv, pname)

        if limit in status.text:
            pack += 1
            pname = f'trzworld{pack}'
            pnick = f"trz's world {pack}"
            edit(message, get_translation('packFull', ['`', '**', str(pack)]))
            return add_exist(conv, pack, pname, pnick)

        send_recv(conv, media, doc=True)
        send_recv(conv, emoji)
        send_recv(conv, '/done')
        return True

    if anim:
        pname += '_anim'
        pnick += ' (Animated)'
    else:
        if not reply.sticker:
            media = resizer(media)

    with PyroConversation(client, 'Stickers') as conv:
        if pack_created():
            ret = add_exist(conv, pack, pname, pnick)
            if not ret:
                return
        else:
            create_new(conv, pack)

    edit(message, get_translation('stickerAdded', ['`', pname]))


def send_recv(conv, msg, doc=False):
    if doc:
        conv.send_doc(msg)
    else:
        conv.send_msg(msg)
    return conv.recv_msg()


@sedenify(pattern='^.getsticker$')
def getsticker(message):
    reply = message.reply_to_message
    if not reply or not reply.sticker:
        edit(message, f'`{get_translation("replySticker")}`')
        return

    photo = download_media_wc(reply)

    reply_doc(
        reply,
        photo,
        caption=f'**Sticker ID:** `{reply.sticker.file_id}'
                f'`\n**Emoji**: `{reply.sticker.emoji}`',
        delete_after_send=True)
    message.delete()


@sedenify(pattern='.packinfo$', compat=False)
def packinfo(client, message):
    reply = message.reply_to_message
    if not reply:
        edit(message, f'`{get_translation("packinfoError")}`')
        return

    if not reply.sticker:
        edit(message, f'`{get_translation("packinfoError2")}`')
        return

    edit(message, f'`{get_translation("packinfoResult")}`')

    get_stickerset = client.send(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=reply.sticker.set_name)))
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    out = get_translation('packinfoResult',
                          ['**',
                           '`',
                           get_stickerset.set.title,
                           get_stickerset.set.short_name,
                           get_stickerset.set.official,
                           get_stickerset.set.archived,
                           get_stickerset.set.animated,
                           get_stickerset.set.count,
                           ' '.join(pack_emojis)])

    edit(message, out)


KOMUT.update({'stickers': get_translation('stickerInfo')})
