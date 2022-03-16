# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#
from requests import get
from json import JSONDecodeError
from sedenbot import HELP, SEDEN_LANG
from sedenecem.core import (
    edit,
    get_translation,
    sedenify,
)


def parseShipEntity(jsonEntity: dict) -> str:
    if SEDEN_LANG == 'en':
        text = f"""
<strong>Company:</strong> <code>{jsonEntity['data']['company'].title()}</code>
<strong>Track ID:</strong> <code>{jsonEntity['data']['tracking_no']}</code>
<strong>Status:</strong> <code>{jsonEntity['data']['status']}</code>
<strong>Sender:</strong> <code>{jsonEntity['data']['sender_name']}</code>
<strong>Receiver:</strong> <code>{jsonEntity['data']['receiver_name']}</code>
<strong>Sender Unit:</strong> <code>{jsonEntity['data']['sender_unit']}</code>
<strong>Receiver Unit:</strong> <code>{jsonEntity['data']['receiver_unit']}</code>
<strong>Sended Date:</strong> <code>{jsonEntity['data']['sended_date']}</code>
<strong>Delivered Date:</strong> <code>{jsonEntity['data']['delivered_date']}</code>

<strong><u>Last movement</u></strong>

"""
    movements = ""
    for movement in jsonEntity['data']['movements'][-1:]:
        movements += f"<code>Unit: {movement['unit']}\nStatus: {movement['status']}\nDate: {movement['date']}\nTime: {movement['time']}\nAction: {movement['action']}</code>\n\n"
    
    if SEDEN_LANG == 'tr':
        text = f"""
<strong>Firma:</strong> <code>{jsonEntity['data']['company'].title()}</code>
<strong>Takip No:</strong> <code>{jsonEntity['data']['tracking_no']}</code>
<strong>Durum:</strong> <code>{jsonEntity['data']['status']}</code>
<strong>Gönderici:</strong> <code>{jsonEntity['data']['sender_name']}</code>
<strong>Alıcı:</strong> <code>{jsonEntity['data']['receiver_name']}</code>
<strong>Gönderim yeri:</strong> <code>{jsonEntity['data']['sender_unit']}</code>
<strong>Alım yeri:</strong> <code>{jsonEntity['data']['receiver_unit']}</code>
<strong>Gönderi tarihi:</strong> <code>{jsonEntity['data']['sended_date']}</code>
<strong>Teslim tarihi:</strong> <code>{jsonEntity['data']['delivered_date']}</code>

<strong><u>Son hareket</u></strong>

"""
    movements = ""
    for movement in jsonEntity['data']['movements'][-1:]:
        movements += f"<code>Yer: {movement['unit']}\nDurum: {movement['status']}\nTarih: {movement['date']}\nZaman: {movement['time']}\nİşlem: {movement['action']}</code>\n\n"
    
    text += movements
    return text


def getShipEntity(company: str, trackId: int or str) -> dict or None:
    headers: dict = {
        'platform': 'Android',
        'public': 'lfJGmU9XpGZcMwyLtZBk',
        'secret': 'sMPMnQuc51nmcBbaeOK1',
        'unique': 'afb612018716663e',
    }
    response = get(f"https://tapi.kolibu.com/{company}/{trackId}", headers=headers)
    try:
        return response.json() if response.json()['success'] else None
    except JSONDecodeError:
        return None

@sedenify(pattern='^.(yurtici|aras|ptt)')
def shippingTrack(message):
    edit(message, f"`{get_translation('processing')}`")
    argv = message.text.split(' ')
    if len(argv) > 2:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return
    comp, trackId = argv
    if not trackId:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return
    if comp == '.yurtici':
        kargo_data = getShipEntity(company="yurtici", trackId=trackId)
    if comp == '.aras':
        kargo_data = getShipEntity(company="aras", trackId=trackId)
    if comp == '.ptt':
        kargo_data = getShipEntity(company="ptt", trackId=trackId)
    if kargo_data:
        text = parseShipEntity(kargo_data)
        edit(message, text, parse='HTML')
        return
    edit(message, '`Tracking information not found!`' if SEDEN_LANG == 'en' else '`Takip bilgisi bulunamadı!`')




HELP.update({'shippingtrack': get_translation("shippingTrack")})