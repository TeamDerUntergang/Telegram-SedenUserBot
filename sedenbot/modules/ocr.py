# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove

from requests import post
from sedenbot import HELP, OCR_APIKEY
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_translation,
    sedenify,
)


def ocr_file(filename, language='eng', overlay=False, api_key=OCR_APIKEY):

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


@sedenify(pattern=r'^.ocr')
def ocr(message):
    if not OCR_APIKEY:
        return edit(
            message,
            get_translation('ocrApiMissing', ['**', 'OCR Space', '`']),
            preview=False,
        )

    match = extract_args(message)
    reply = message.reply_to_message

    if len(match) < 1:
        return edit(message, f'`{get_translation("wrongCommand")}`')

    if not reply.media:
        return edit(message, f'`{get_translation("wrongCommand")}`')

    edit(message, f'`{get_translation("ocrReading")}`')
    lang_code = extract_args(message)
    downloaded_file_name = download_media_wc(reply, sticker_orig=True)
    test_file = ocr_file(downloaded_file_name, lang_code)

    try:
        ParsedText = test_file['ParsedResults'][0]['ParsedText']
    except BaseException:
        edit(message, f'`{get_translation("ocrError")}`')
    else:
        edit(message, get_translation('ocrResult', ['`', ParsedText]))
    remove(downloaded_file_name)


HELP.update({'ocr': get_translation('ocrInfo')})
