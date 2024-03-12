# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import JSONDecodeError
from re import sub
from typing import Union

from pyrogram import enums
from requests import post
from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args_split,
    get_translation,
    parse_cmd,
    sedenify,
)


def format_datetime(datetime_str):
    if datetime_str:
        date_part, time_part = datetime_str.split('T')
        formatted_datetime = f"{date_part} {time_part.replace(':', ':')}"
        return formatted_datetime
    else:
        return None


def format_prefix(text):
    if text:
        if ":" in text:
            formatted_text = sub(r':\s*', ':', text).split(':', 1)[-1].strip()
        else:
            formatted_text = text
    else:
        formatted_text = None
    return formatted_text


def parseShipEntity(jsonEntity: dict) -> str:
    if not jsonEntity['value'][0]['success']:
        return '<code>Kargo bulunamadı</code>'
    else:
        text = (
            f"<b>Firma:</b> <code>{jsonEntity['value'][0]['value']['companyName']}</code>\n"
            f"<b>Takip No:</b> <code>{jsonEntity['value'][0]['value']['barcode']}</code>\n"
            f"<b>Durum:</b> <code>{jsonEntity['value'][0]['value']['statusDescription']}</code>\n"
            f"<b>Gönderici:</b> <code>{format_prefix(jsonEntity['value'][0]['value']['sender']) or 'Bulunamadı'}</code>\n"
            f"<b>Alıcı:</b> <code>{format_prefix(jsonEntity['value'][0]['value']['receiver']) or 'Bulunamadı'}</code>\n"
            f"<b>Gönderim Yeri:</b> <code>{format_prefix(jsonEntity['value'][0]['value']['senderAddress']) or 'Bulunamadı'}</code>\n"
            f"<b>Alım Yeri:</b> <code>{format_prefix(jsonEntity['value'][0]['value']['receiverAddress']) or 'Bulunamadı'}</code>\n"
            f"<b>Gönderi Tarihi:</b> <code>{format_datetime(jsonEntity['value'][0]['value']['sendDate']) or 'Bulunamadı'}</code>\n"
            f"<b>Teslim Tarihi:</b> <code>{format_datetime(jsonEntity['value'][0]['value']['deliveredDate']) or 'Bulunamadı'}</code>"
        )
        if jsonEntity['value'][0]['value']['movement']:
            last_movement = jsonEntity['value'][0]['value']['movement'][-1]
            movements = (
                f"\n\n<b><u>Son hareketler</u></b>\n\n"
                f"<code>Yer: {format_prefix(last_movement['externalLocation'])}</code>\n"
                f"<code>Durum: {last_movement['title']}</code>\n"
                f"<code>Tarih: {format_datetime(last_movement['date'])}</code>\n"
            )
            text += movements
        return text


def getShipEntity(company: str, trackId: Union[int, str]):
    url = 'https://kargomnerede.com.tr/api/search-codes'
    data = {"barcodes": [{"companyId": company, "code": trackId}]}

    try:
        response = post(url, json=data)
        return response.json() if response.json()['success'] else None
    except JSONDecodeError:
        return None


@sedenify(pattern='^.(hepsijet|yurti[cç]i|(s[uü]ra|pt)t|aras|mng|ups)')
def shippingTrack(message):
    edit(message, f"`{get_translation('processing')}`")
    trackId = extract_args_split(message)
    comp = parse_cmd(message.text)
    if not trackId or len(trackId) > 1:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return
    match comp.replace('ç', 'c').replace('ü', 'u'):
        case 'yurtici':
            kargo_data = getShipEntity(company='2', trackId=trackId[0])
        case 'aras':
            kargo_data = getShipEntity(company='1', trackId=trackId[0])
        case 'ptt':
            kargo_data = getShipEntity(company='4', trackId=trackId[0])
        case 'mng':
            kargo_data = getShipEntity(company='3', trackId=trackId[0])
        case 'ups':
            kargo_data = getShipEntity(company='5', trackId=trackId[0])
        case 'surat':
            kargo_data = getShipEntity(company='6', trackId=trackId[0])
        case 'hepsijet':
            kargo_data = getShipEntity(company='10', trackId=trackId[0])
    if kargo_data:
        text = parseShipEntity(kargo_data)
        edit(message, text, parse=enums.ParseMode.HTML)
        return
    edit(message, f"`{get_translation('shippingNoResult')}`")


HELP.update({'shippingtrack': get_translation('shippingTrack')})
