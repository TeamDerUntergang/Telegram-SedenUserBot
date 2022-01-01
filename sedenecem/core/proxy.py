# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from bs4 import BeautifulSoup
from requests import get
from sedenbot import TEMP_SETTINGS, get_translation

from .misc import edit


def use_proxy(message) -> None:
    edit(message, f'`{get_translation("fetchProxy")}`')
    proxy = get_random_proxy()
    edit(message, f'`{get_translation("providedProxy")}`')
    return proxy


def get_stored_proxy():
    return TEMP_SETTINGS.get('VALID_PROXY_URL', '')


def put_stored_proxy(proxy):
    TEMP_SETTINGS['VALID_PROXY_URL'] = proxy


def _xget_random_proxy():
    proxy = get_stored_proxy()
    try_valid = tuple(proxy.split(":")) if len(proxy) else None
    if try_valid:
        valid = _try_proxy(try_valid)
        if valid[0] == 200 and "<title>Too" not in valid[1]:
            return try_valid

    head = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'ArabyBot (compatible; Mozilla/5.0; GoogleBot; FAST Crawler 6.4; http://www.araby.com;)',
        'Referer': 'https://www.google.com/search?q=sslproxies',
    }

    req = get('https://sslproxies.org/', headers=head)
    soup = BeautifulSoup(req.text, 'html.parser')
    res = soup.find('div', {'class': 'fpl-list'}).find('tbody')
    res = res.findAll('tr')
    for item in res:
        infos = item.findAll('td')
        ip = infos[0].text
        port = infos[1].text
        proxy = (ip, port)
        if _try_proxy(proxy)[0] == 200:
            return proxy

    return None


def _try_proxy(proxy):
    try:
        prxy = f'http://{proxy[0]}:{proxy[1]}'
        req = get(
            'https://www.gsmarena.com/',
            proxies={'http': prxy, 'https': prxy},
            timeout=1,
        )
        if req.status_code == 200:
            return (200, req.text)
        raise Exception
    except BaseException:
        return (404, None)


def get_random_proxy():
    proxy = _xget_random_proxy()
    if not proxy:
        return None
    proxy = f'http://{proxy[0]}:{proxy[1]}'
    put_stored_proxy(proxy)

    proxy_dict = {
        'https': proxy,
        'http': proxy,
    }

    return proxy_dict
