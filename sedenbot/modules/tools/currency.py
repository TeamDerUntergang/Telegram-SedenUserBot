# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from bs4 import BeautifulSoup
from requests import get

from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, sedenify, useragent


@sedenify(pattern='^.currency')
def currency_convert(message):
    input_str = extract_args(message)
    input_sgra = input_str.split(' ')
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = f'https://www.x-rates.com/calculator/?from={currency_from}&to={currency_to}&amount={number}'
            current_response = get(request_url, headers={'User-Agent': useragent()})
            if current_response.status_code == 200:
                soup = BeautifulSoup(current_response.text, 'html.parser')
                rebmun = soup.find('span', {'class': 'ccOutputRslt'})
                result = rebmun.find('span')
                result.extract()
                edit(message, f'**{number} {currency_from} = {rebmun.text.strip()}**')
            else:
                edit(message, f'`{get_translation("currencyError")}`')
        except Exception as e:
            edit(message, str(e))
    else:
        edit(message, f'`{get_translation("syntaxError")}`')
        return


@sedenify(pattern='^.d[oö]viz')
def doviz(message):
    req = get(
        'https://www.doviz.com/',
        headers={'User-Agent': useragent()},
    )
    page = BeautifulSoup(req.content, 'html.parser')
    res = page.find_all('div', {'class': 'item'})
    out = '**Güncel döviz kurları:**\n\n'

    for item in res:
        name = item.find('span', {'class': 'name'}).text
        value = item.find('span', {'class': 'value'}).text

        rate_elem = item.find(
            'div', {'class': ['change-rate status down', 'change-rate status up']}
        )
        rate_class = rate_elem['class'][-1] if rate_elem else None

        changes_emoji = ''
        if rate_class == 'down':
            changes_emoji = '⬇️'
        elif rate_class == 'up':
            changes_emoji = '⬆️'

        if changes_emoji:
            out += f'{changes_emoji} **{name}:** `{value}`\n'
        else:
            out += f'**{name}:** `{value}`\n'

    edit(message, out)


HELP.update({'currency': get_translation('currencyInfo')})
