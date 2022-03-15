# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from ast import arg
from requests import get, post
from json import JSONDecodeError
from sedenbot import HELP, SEDEN_LANG
from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    sedenify,
)




def getSession():
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip',
        'accept-language': 'tr',
        'host': 'customerappapi.yurticikargo.com',
        'user-agent': 'okhttp/4.4.0',
        'yk-app-token': 'Android407',
        'yk-mobile-device-id': 'd2926855-ed39-4f05-afcf-a9f350829427',
        'yk-mobile-os': 'Android',}

    response = post('https://customerappapi.yurticikargo.com/KOPSRestServices/rest/customermobile/auth/session', headers=headers)
    return response.json()['sessionToken']

def getKargoEntity(kargoId):
    try:
        headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip',
        'authorization': getSession(),
        'user-agent': 'okhttp/4.4.0',
        'yk-app-token': 'Android407',
        'yk-mobile-device-id': 'd2926855-ed39-4f05-afcf-a9f350829427',
        'yk-mobile-os': 'Android',
        'accept-language': 'tr',
        }
        response = get(f'https://customerappapi.yurticikargo.com/KOPSRestServices/rest/customermobile/shipments/tracking/{kargoId}/detail', headers=headers).json()
        return response
    except JSONDecodeError:
        return None


@sedenify(pattern='^.yurtici')
def yurticiKargo(message):
    edit(message, f"`{get_translation('processing')}`")
    argv = extract_args(message)
    takipNo = argv.split(' ', 1)[0]
    if not takipNo or len(takipNo) != 12:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return
    dateParse = lambda raw_date: "{}.{}.{}".format(*[raw_date[:4], raw_date[4:6], raw_date[6:8]])
    kargo_data = getKargoEntity(takipNo)
    text = f"""
<strong>Firma:</strong> <code>Yurtici Kargo</code>
<strong>Durum:</strong> <code>{kargo_data['shipmentStatus'].title()}</code>
<strong>Gönderen:</strong> <code>{kargo_data['sender'].replace("******************", "")}</code>
<strong>Alıcı:</strong> <code>{kargo_data['receiver'].replace("******************", "")}</code>
<strong>Tahmini Teslim:</strong> <code>{dateParse(kargo_data['estimatedDeliveryDate'])}</code>
<strong>Çıkış Tarihi:</strong> <code>{dateParse(kargo_data['shipmentDate'])}</code>
<strong>Gönderi Kodu:</strong> <code>{kargo_data['id']}</code>
<strong>Teslim Birimi:</strong> <code>{kargo_data['deliveryUnitName']}</code>
"""
    edit(message, text, parse='HTML')




HELP.update({'kargotakip': get_translation("shippingTrack")})