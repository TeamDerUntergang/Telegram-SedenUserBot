# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from requests import get

from sedenbot import KOMUT, WEATHER, SEDEN_LANG
from sedenecem.core import edit, extract_args, sedenify, get_translation

# ===== CONSTANT =====
if WEATHER:
    DEFCITY = WEATHER
else:
    DEFCITY = None
# ====================
# Copyright (c) @frknkrc44 | 2020


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
        edit(message, f'`{data}`', fix_markdown=True)
    except Exception as e:
        edit(message, f'`{get_translation("weatherErrorServer")}`')
        raise e


KOMUT.update({"havadurumu": get_translation('infoWeather')})
