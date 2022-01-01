# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove

from barcode import get
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image
from sedenbot import HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_download_dir,
    get_translation,
    reply_sticker,
    sedenify,
)
from urllib3 import PoolManager

from qrcode import QRCode, constants


@sedenify(pattern='^.decode$')
def parseqr(message):
    reply = message.reply_to_message
    if (
        reply
        and reply.media
        and (
            reply.photo
            or (reply.sticker and not reply.sticker.is_animated)
            or (reply.document and 'image' in reply.document.mime_type)
        )
    ):
        edit(message, f'`{get_translation("processing")}`')
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    output = download_media_wc(reply, f'{get_download_dir()}/decode.png')

    if reply.sticker and not reply.sticker.is_animated:
        image = Image.open(output)
        output = f'{get_download_dir()}/decode.png'
        image.save(output)

    dw = open(output, 'rb')
    files = {'f': dw.read()}
    t_response = None

    try:
        http = PoolManager()
        t_response = http.request('POST', 'https://zxing.org/w/decode', fields=files)
        t_response = t_response.data
        http.clear()
        dw.close()
    except BaseException:
        pass

    remove(output)
    if not t_response:
        edit(message, f'`{get_translation("decodeFail")}`')
        return
    try:
        soup = BeautifulSoup(t_response, 'html.parser')
        qr_contents = soup.find_all('pre')[0].text
        edit(message, qr_contents)
    except BaseException:
        edit(message, f'`{get_translation("decodeFail")}`')


@sedenify(pattern='^.barcode')
def barcode(message):
    input_str = extract_args(message)
    reply = message.reply_to_message
    if len(input_str) < 1:
        edit(message, get_translation('barcodeUsage', ['**', '`']))
        return
    edit(message, f'`{get_translation("processing")}`')
    try:
        bar_code_mode_f = get('code128', input_str, writer=ImageWriter())
        filename = bar_code_mode_f.save('code128')
        image = Image.open(filename)
        filename = f'{get_download_dir()}/barcode.webp'
        image.save(filename)
        reply_sticker(reply or message, filename, delete_file=True)
        message.delete()
        remove('code128.png')
    except Exception as e:
        edit(message, str(e))
        return


@sedenify(pattern='^.makeqr')
def makeqr(message):
    input_str = extract_args(message)
    reply = message.reply_to_message
    if len(input_str) < 1:
        edit(message, get_translation('makeqrUsage', ['**', '`']))
        return
    edit(message, f'`{get_translation("processing")}`')
    try:
        qr = QRCode(
            version=1, error_correction=constants.ERROR_CORRECT_L, box_size=10, border=4
        )
        qr.add_data(input_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        output = f'{get_download_dir()}/qrcode.webp'
        img.save(output)
        reply_sticker(reply or message, output, delete_file=True)
        message.delete()
    except Exception as e:
        edit(message, str(e))
        return


HELP.update({'qrcode': get_translation('makeqrInfo')})
HELP.update({'barcode': get_translation('barcodeInfo')})
