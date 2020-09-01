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

from os import path, remove
from removebg import RemoveBg

from sedenbot import KOMUT, RBG_APIKEY, DOWNLOAD_DIRECTORY
from sedenecem.core import sedenify, edit, reply_doc

@sedenify(pattern='^.rbg$', compat=False)
def rbg(client, message):
    if not RBG_APIKEY:
        edit(message, '**[Remove.BG](https://www.remove.bg/api)** `API key eksik! Lütfen ekleyin.`',
             preview=False)
        return

    reply = message.reply_to_message

    if reply and (reply.photo or (reply.document and 'image' in reply.document.mime_typereply.document)):
        edit(message, '`İşleniyor...`')
    else:
        edit(message, '`Bir görüntüye yanıt verin...`')
        return

    IMG_PATH = f'{DOWNLOAD_DIRECTORY}/image.png'

    if path.exists(IMG_PATH):
        remove(IMG_PATH)
    client.download_media(message=reply, file_name=IMG_PATH)
    edit(message, '`Bu görüntüden arka plan kaldırılıyor..`')
    try:
        remove_bg = RemoveBg(RBG_APIKEY, 'hata.log')
        remove_bg.remove_background_from_img_file(IMG_PATH)
        rbg_img = IMG_PATH + '_no_bg.png'
        reply_doc(reply, rbg_img,
                  caption='Remove.bg kullanılarak arka plan kaldırıldı')
        message.delete()
    except Exception as e:
        raise e

KOMUT.update({
    "rbg":
    ".rbg herhangi bir fotoğrafı yanıtlayın (Uyarı: çıkartmalar üzerinde çalışmaz.)\
\nKullanım: Remove.bg API kullanarak görüntülerin arka planını kaldırır."
})
