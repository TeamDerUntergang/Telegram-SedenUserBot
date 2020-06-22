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

import os

from requests import post

from sedenbot import KOMUT, DOWNLOAD_DIRECTORY, OCR_APIKEY
from sedenecem.events import edit, extract_args, sedenify

def ocr_file(filename,
                    overlay=False,
                    api_key=OCR_APIKEY,
                    language='tur'):

    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()

@sedenify(pattern=r'^.ocr', compat=False)
def ocr(client, message):
    edit(message, '`Okunuyor...`')
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
    lang_code = extract_args(message)
    downloaded_file_name = client.download_media(
        message.reply_to_message, DOWNLOAD_DIRECTORY)
    test_file = ocr_file(filename=downloaded_file_name,
                                    language=lang_code)
    try:
        ParsedText = test_file['ParsedResults'][0]['ParsedText']
    except BaseException:
        edit(message, '`Bunu okuyamadım.`\n`Sanırım yeni gözlüklere ihtiyacım var.`')
    else:
        edit(message, f'`İşte okuyabildiğim şey:`\n\n{ParsedText}'
                         )
    os.remove(downloaded_file_name)

KOMUT.update({
    'ocr':
    ".ocr <dil>\nKullanım: Metin ayıklamak için bir resme veya çıkartmaya cevap verin.\n\nDil kodlarını [buradan](https://ocr.space/ocrapi) alın."
})
