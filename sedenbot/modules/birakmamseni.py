# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from requests import post
from sedenbot import HELP
from sedenecem.core import edit, sedenify, get_translation


@sedenify(pattern='^.b[ıi]rakmamseni$')
def birakmamseni(message):
    '''Copyright (c) @Adem68 | 2020'''
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

    sonuc = get_translation('birakmamseniResult', ['**', '`', count])

    edit(message, sonuc, preview=False)


HELP.update({'birakmamseni': get_translation('birakmamseniInfo')})
