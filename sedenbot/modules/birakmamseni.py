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
#

from requests import post
from sedenbot import KOMUT
from sedenecem.core import edit, sedenify, get_translation


@sedenify(pattern='^.b[ıi]rakmamseni$')
def birakmamseni(message):
    """Copyright (c) @Adem68 | 2020"""
    url = 'https://birakmamseni.org/'
    path = 'api/counter'

    headers = {
        'User-Agent': 'ajax/7.66.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': '{}'.format(url),
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        response = post(url=url + path, headers=headers)
        count = response.json()['counter'].lstrip('0')
    except BaseException:
        edit(message, f'`{get_translation("covidError")}`')
        return

    sonuc = (get_translation("birakmamseniResult", ['**', '`', count]))

    edit(message, sonuc, preview=False)


KOMUT.update({"birakmamseni": get_translation("birakmamseniInfo")})
