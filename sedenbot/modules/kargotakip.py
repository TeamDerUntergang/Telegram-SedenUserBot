# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import JSONDecodeError

from pyrogram import enums
from requests import get
from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args_split,
    get_translation,
    parse_cmd,
    sedenify,
)


def parseShipEntity(jsonEntity: dict) -> str:
    text = get_translation(
        'shippingResult',
        [
            '<b>',
            '</b>',
            '<code>',
            '</code>',
            jsonEntity['data']['company'].title(),
            jsonEntity['data']['tracking_no'],
            jsonEntity['data']['status'],
            jsonEntity['data']['sender_name'],
            jsonEntity['data']['receiver_name'],
            jsonEntity['data']['sender_unit'],
            jsonEntity['data']['receiver_unit'],
            jsonEntity['data']['sended_date'],
            jsonEntity['data']['delivered_date'] or get_translation('notFound'),
        ],
    )
    if jsonEntity['data']['movements']:
        movements = get_translation(
            'shippingMovements',
            [
                '<b>',
                '</b>',
                '<u>',
                '</u>',
                '<code>',
                '</code>',
                jsonEntity['data']['movements'][0]['unit'],
                jsonEntity['data']['movements'][0]['status'],
                jsonEntity['data']['movements'][0]['date'],
                jsonEntity['data']['movements'][0]['time'],
                jsonEntity['data']['movements'][0]['action'],
            ],
        )

        text += movements
    return text


def getShipEntity(company: str, trackId: int or str) -> dict or None:
    headers: dict = {
        'platform': 'Android',
        'public': 'lfJGmU9XpGZcMwyLtZBk',
        'secret': 'sMPMnQuc51nmcBbaeOK1',
        'unique': 'afb612018716663e',
    }
    response = get(f'https://tapi.kolibu.com/{company}/{trackId}', headers=headers)
    try:
        return response.json() if response.json()['success'] else None
    except JSONDecodeError:
        return None


@sedenify(pattern='^.(hepsijet|trendyol|yurti[cç]i|(s[uü]ra|pt)t|aras|mng|ups)')
def shippingTrack(message):
    edit(message, f"`{get_translation('processing')}`")
    trackId = extract_args_split(message)
    comp = parse_cmd(message.text)
    if not trackId or len(trackId) > 1:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return
    match comp.replace('ç', 'c').replace('ü', 'u'):
        case 'yurtici':
            kargo_data = getShipEntity(company='yurtici', trackId=trackId[0])
        case 'aras':
            kargo_data = getShipEntity(company='aras', trackId=trackId[0])
        case 'ptt':
            kargo_data = getShipEntity(company='ptt', trackId=trackId[0])
        case 'mng':
            kargo_data = getShipEntity(company='mng', trackId=trackId[0])
        case 'ups':
            kargo_data = getShipEntity(company='ups', trackId=trackId[0])
        case 'surat':
            kargo_data = getShipEntity(company='surat', trackId=trackId[0])
        case 'trendyol':
            kargo_data = getShipEntity(company='trendyolexpress', trackId=trackId[0])
        case 'hepsijet':
            kargo_data = getShipEntity(company='hepsijet', trackId=trackId[0])
    if kargo_data:
        text = parseShipEntity(kargo_data)
        edit(message, text, parse=enums.ParseMode.HTML)
        return
    edit(message, f"`{get_translation('shippingNoResult')}`")


HELP.update({'shippingtrack': get_translation('shippingTrack')})
