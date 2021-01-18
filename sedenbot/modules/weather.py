# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from requests import get

from sedenbot import HELP, WEATHER, SEDEN_LANG
from sedenecem.core import edit, extract_args, sedenify, get_translation

# ===== CONSTANT =====
if WEATHER:
    DEFCITY = WEATHER
else:
    DEFCITY = None
# ====================


@sedenify(pattern='^.(havadurumu|w(eathe|tt)r)')
def havadurumu(message):
    args = extract_args(message)

    if len(args) < 1:
        CITY = DEFCITY
        if not CITY:
            edit(message, f'`{get_translation("weatherErrorCity")}`')
            return
    else:
        CITY = args

    if ',' in CITY:
        CITY = CITY[:CITY.find(',')].strip()

    try:
        req = get(
            f'http://wttr.in/{CITY}?mqT0',
            headers={
                'User-Agent': 'curl/7.66.0',
                'Accept-Language': SEDEN_LANG})
        data = req.text
        if '===' in data:
            raise Exception
        data = data.replace('`', '‛')
        edit(message, f'`{data}`')
    except Exception as e:
        edit(message, f'`{get_translation("weatherErrorServer")}`')
        raise e


HELP.update({'weather': get_translation('infoWeather')})
