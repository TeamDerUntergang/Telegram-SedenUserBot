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

from random import choice
from requests import get

from sedenbot import me
from sedenecem.conv import PyroConversation
from sedenecem.core import edit, sedenify, download_media, extract_args, sticker_resize as resizer
# ================= CONSTANT =================
DIZCILIK = [
    "Çıkartmayı dızlıyorum...",
    "Yaşasın dızcılık...",
    "Bu çıkartmayı kendi paketime davet ediyorum...",
    "Bunu dızlamam lazım...",
    "Hey bu güzel bir çıkartma!\nHemen dızlıyorum...",
    "Çıkartmanı dızlıyorum\nhahaha.",
    "Hey şuraya bak. (☉｡☉)!→\nBen bunu dızlarken...",
    "Güller kırmızı menekşeler mavi, bu çıkartmayı paketime dızlayarak havalı olacağım...",
    "Çıkartma hapsediliyor...",
    "Bay dızcı bu çıkartmayı dızlıyor...",
    "Sonunda Ecem'in seveceği bir çıkartma dızlıyorum...",
    "Ecem, bu dız senin için...",
]
# ================= CONSTANT =================
# Copyright (c) @NaytSeyd, @frknkrc44 | 2020
@sedenify(pattern='^.(d[ıi]zla|kang)', compat=False)
def kang(client, message):
    myacc = me[0]
    kanger = myacc.username or myacc.first_name
    if myacc.username:
        kanger = f'@{kanger}'
    pack = extract_args(message)

    reply = message.reply_to_message
    if not reply:
        edit(message, '`Bana dızlayabileceğim bir şey ver.`')
        return

    anim = False
    media = None

    if(reply.photo or reply.document or reply.sticker):
        edit(message, f'`{choice(DIZCILIK)}`')
        media = download_media(client, reply)
        anim = reply.sticker and reply.sticker.is_animated
    else:
        edit(message, '`Bunu dızlayamam.`')
        return

    if len(pack) < 1:
        pack = 1

    emoji = '🤤'

    if ' ' in str(pack):
        emoji, pack = pack.split(' ', 1)

    pack = 1 if not str(pack).isdigit() else int(pack)

    pname = f'a{myacc.id}_by_{myacc.username}_{pack}'
    pnick = f"{kanger}'s UserBot pack {pack}"

    limit = '50' if anim else '120'

    def pack_created():
        created = get(f'https://telegram.me/addstickers/{pname}')
        created = (('A <strong>Telegram</strong> user has created the '
                    '<strong>Sticker&nbsp;Set</strong>') not in created.text)
        return created

    def create_new(conv):
        cmd = f'/new{"animated" if anim else "pack"}'

        try:
            send_recv(conv, cmd)
        except Exception as e:
            raise e
        msg = send_recv(conv, pnick)
        if msg.text == 'Invalid pack selected.':
            pack += 1
            return create_new(conv)
        send_recv(conv, media, doc=True)
        send_recv(conv, emoji)
        send_recv(conv, '/publish')
        if anim:
            send_recv(conv, f'<{pnick}>')
        send_recv(conv, '/skip')
        send_recv(conv, pname)

    def add_exist(conv):
        try:
            send_recv(conv, '/addsticker')
        except Exception as e:
            raise e

        status = send_recv(conv, pname)

        if limit in status.text:
            edit(message, f'`{pack} numaralı paket dolu.`')
            return False

        send_recv(conv, media, doc=True)
        send_recv(conv, emoji)
        send_recv(conv, '/done')
        return True

    if anim:
        name += '_anim'
        nick = ' (Animasyonlu)'
    else:
        media = resizer(media)

    with PyroConversation(client, 'Stickers') as conv:
        if pack_created():
            ret = add_exist(conv)
            if not ret:
                return
        else:
            create_new(conv)

    edit(message, f'Başarıyla dızlandı, erişmek için [buraya](https://telegram.me/addstickers/{pname}) dokunun.')


def send_recv(conv, msg, doc=False):
    if doc:
        conv.send_doc(msg)
    else:
        conv.send_msg(msg)
    return conv.recv_msg()
