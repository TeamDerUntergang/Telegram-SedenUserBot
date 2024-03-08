# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from re import findall

from pyrogram import enums
from requests import post

from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, sedenify


@sedenify(pattern='^.imei(|check)')
def imeichecker(message):
    imei = extract_args(message)
    edit(message, f'`{get_translation("processing")}`')
    if len(imei) != 15:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    try:
        while True:
            response = post(
                f"https://m.turkiye.gov.tr/api2.php?p=imei-sorgulama&txtImei={imei}"
            ).json()
            if not response['data']['asyncFinished']:
                continue
            result = response['data']
            break
        _marka = findall(r'Marka:(.+) Model', result['markaModel'])
        _model = findall(r'Model Bilgileri:(.+)', result['markaModel'])
        _pazaradi = findall(r'Pazar Adı:(.+) Marka', result['markaModel'])
        marka = _marka[0].replace(',', '').strip() if _marka else None
        model = _model[0].replace(',', '').strip() if _model else None
        pazaradi = _pazaradi[0].replace(',', '').strip() if _pazaradi else None
        reply_text = f"<b>Sorgu Tarihi:</b> <code>{result['sorguTarihi']}</code>\n\n"
        reply_text += f"<b>IMEI:</b> <code>{result['imei'][:-5]+5*'*'}</code>\n"
        reply_text += f"<b>Durum:</b> <code>{result['durum']}</code>\n"
        reply_text += f"<b>Kaynak:</b> <code>{result['kaynak']}</code>\n"
        reply_text += (
            f"<b>Pazar Adı:</b> <code>{pazaradi}</code>\n"
            if pazaradi is not None
            else ""
        )
        reply_text += (
            f"<b>Marka:</b> <code>{marka}</code>\n" if marka is not None else ""
        )
        reply_text += (
            f"<b>Model:</b> <code>{model}</code>\n\n" if model is not None else ""
        )

        edit(message, reply_text, parse=enums.parse_mode.ParseMode.HTML, preview=False)
    except Exception as e:
        raise e


HELP.update({'imeicheck': get_translation('imeiInfo')})
