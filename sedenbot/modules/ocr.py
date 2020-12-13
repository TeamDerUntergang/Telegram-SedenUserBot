# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove, path, makedirs
from requests import post

from sedenbot import KOMUT, DOWNLOAD_DIRECTORY, OCR_APIKEY
from sedenecem.core import edit, extract_args, sedenify, get_translation


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
    if not OCR_APIKEY:
        edit(
            message, get_translation(
                'ocrApiMissing', [
                    '**', 'OCR Space', '`']), preview=False)
        return
    match = extract_args(message)
    if len(match) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    edit(message, f'`{get_translation("ocrReading")}`')
    if not path.isdir(DOWNLOAD_DIRECTORY):
        makedirs(DOWNLOAD_DIRECTORY)
    lang_code = extract_args(message)
    downloaded_file_name = client.download_media(
        message.reply_to_message, DOWNLOAD_DIRECTORY)
    test_file = ocr_file(filename=downloaded_file_name,
                         language=lang_code)
    try:
        ParsedText = test_file['ParsedResults'][0]['ParsedText']
    except BaseException:
        edit(message, f'`{get_translation("ocrError")}`')
    else:
        edit(message, get_translation('ocrResult', ['`', ParsedText]))
    remove(downloaded_file_name)


KOMUT.update({'ocr': get_translation('ocrInfo')})
