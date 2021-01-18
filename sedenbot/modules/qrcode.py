# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove
from qrcode import QRCode, constants
from barcode import get
from barcode.writer import ImageWriter
from urllib3 import PoolManager
from bs4 import BeautifulSoup

from sedenbot import HELP
from sedenecem.core import (extract_args, sedenify, edit, reply_doc,
                            download_media_wc, get_translation)


@sedenify(pattern=r'^.decode$')
def parseqr(message):
    reply = message.reply_to_message
    if not(reply.photo or reply.sticker or (
            reply.document and 'image' in reply.document.mime_type)):
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    downloaded_file_name = download_media_wc(reply)

    dw = open(downloaded_file_name, 'rb')
    files = {'f': dw.read()}
    t_response = None

    try:
        http = PoolManager()
        t_response = http.request(
            'POST', 'https://zxing.org/w/decode', fields=files)
        t_response = t_response.data
        http.clear()
        dw.close()
    except BaseException:
        pass

    remove(downloaded_file_name)
    if not t_response:
        edit(message, f'`{get_translation("decodeFail")}`')
        return
    try:
        soup = BeautifulSoup(t_response, 'html.parser')
        qr_contents = soup.find_all('pre')[0].text
        edit(message, qr_contents)
    except BaseException:
        edit(message, f'`{get_translation("decodeFail")}`')


@sedenify(pattern=r'^.barcode')
def barcode(message):
    input_str = extract_args(message)
    usage = get_translation('barcodeUsage', ['**', '`'])
    reply = message.reply_to_message
    if len(input_str) < 1 and not reply:
        edit(message, usage)
        return
    edit(message, f'`{get_translation("processing")}`')
    if reply:
        if reply.media:
            downloaded_file_name = download_media_wc(reply)
            media_list = None
            with open(downloaded_file_name, 'rb') as file:
                media_list = file.readlines()
            qrmsg = ''
            for media in media_list:
                qrmsg += media.decode('UTF-8') + '\r\n'
            remove(downloaded_file_name)
        else:
            qrmsg = reply
    else:
        qrmsg = input_str

    bar_code_type = 'code128'
    try:
        bar_code_mode_f = get(bar_code_type, qrmsg, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        reply_doc(message, filename, delete_after_send=True)
    except Exception as e:
        edit(message, str(e))
        return
    message.delete()


@sedenify(pattern=r'^.makeqr')
def makeqr(message):
    input_str = extract_args(message)
    usage = get_translation('makeqrUsage', ['**', '`'])
    reply = message.reply_to_message
    if len(input_str) < 1 and not reply:
        edit(message, usage)
        return
    edit(message, f'`{get_translation("processing")}`')
    if reply:
        if reply.media:
            downloaded_file_name = download_media_wc(reply)
            media_list = None
            with open(downloaded_file_name, 'rb') as file:
                media_list = file.readlines()
            qrmsg = ''
            for media in media_list:
                qrmsg += media.decode('UTF-8') + '\r\n'
            remove(downloaded_file_name)
        else:
            qrmsg = reply
    else:
        qrmsg = input_str

    try:
        qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4)
        qr.add_data(qrmsg)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img.save('img_file.webp', 'PNG')
        reply_doc(message, 'img_file.webp', delete_after_send=True)
    except Exception as e:
        edit(message, str(e))
        return
    message.delete()


HELP.update({'qrcode': get_translation('makeqrInfo')})
HELP.update({'barcode': get_translation('barcodeInfo')})
