# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
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

from .misc import edit, useragent


class ProxyHandler:
    """
    A class for handling the retrieval and use of HTTP proxies.

    Attributes:
        proxy (Union[None, dict[str, str]]): The current proxy to be used for HTTP requests.

    Methods:
        use_proxy(message: Message) -> Union[None, dict[str, str]]:
            Retrieves a valid proxy and returns it as a dictionary containing 'http' and 'https' keys.

        get_stored_proxy() -> str:
            Retrieves the stored proxy URL from temporary settings.

        put_stored_proxy(proxy: str) -> None:
            Sets the stored proxy URL in temporary settings.

        _xget_random_proxy() -> Union[None, tuple[str, str]]:
            Attempts to retrieve a random proxy URL from the SSL Proxies website.

        _try_proxy(proxy: tuple[str, str]) -> tuple[int, Union[str, None]]:
            Tests the provided proxy to ensure that it can be used for HTTP requests.

        get_random_proxy() -> Union[None, dict[str, str]]:
            Retrieves a random, valid proxy URL and sets it as the current proxy for HTTP requests.

    Usage:
        handler = ProxyHandler()
        proxy = handler.use_proxy("Fetching proxy...")
        req = requests.get("https://www.example.com", proxies=proxy)
    """

    def __init__(self):
        self.proxy = None

    def use_proxy(self, message) -> None:
        edit(message, f'`{get_translation("fetchProxy")}`')
        proxy = self.get_random_proxy()
        edit(message, f'`{get_translation("providedProxy")}`')
        return proxy

    def get_stored_proxy(self):
        return TEMP_SETTINGS.get('VALID_PROXY_URL', '')

    def put_stored_proxy(self, proxy):
        TEMP_SETTINGS['VALID_PROXY_URL'] = proxy

    def _xget_random_proxy(self):
        proxy = self.get_stored_proxy()
        try_valid = tuple(proxy.split(":")) if len(proxy) else None
        if try_valid:
            valid = self._try_proxy(try_valid)
            if valid[0] == 200 and "<title>Too" not in valid[1]:
                return try_valid

        head = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': useragent(),
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
            if self._try_proxy(proxy)[0] == 200:
                return proxy

        return None

    def _try_proxy(self, proxy):
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

    def get_random_proxy(self):
        proxy = self._xget_random_proxy()
        if not proxy:
            return None
        proxy = f'http://{proxy[0]}:{proxy[1]}'
        self.put_stored_proxy(proxy)

        proxy_dict = {
            'https': proxy,
            'http': proxy,
        }

        return proxy_dict
