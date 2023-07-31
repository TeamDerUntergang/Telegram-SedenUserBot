# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from requests import get
from sedenbot import HELP, SEDEN_LANG, WEATHER
from sedenecem.core import edit, extract_args, get_translation, sedenify

# ===== CONSTANT =====
DEFAULT_CITY = WEATHER.capitalize() if WEATHER else None
# ====================


@sedenify(pattern='^.(hava(|durumu)|w(eathe|tt)r)')
def weather(message):
    args = extract_args(message).capitalize()

    CITY = DEFAULT_CITY if len(args) < 1 else args.split(',')[0].strip()

    try:
        response = get(
            f'http://wttr.in/{CITY}?mQT0',
            headers={'User-Agent': 'curl/7.66.0', 'Accept-Language': SEDEN_LANG},
        )
        data = response.text
        if '===' in data or '404' in data:
            raise Exception
        data = data.replace('`', '‛')
        edit(message, f'**{CITY}**\n\n`{data}`')
    except Exception:
        edit(message, f'`{get_translation("weatherErrorServer")}`')


HELP.update({'weather': get_translation('infoWeather')})
