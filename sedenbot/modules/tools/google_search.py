# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from random import choice
from re import findall, sub
from traceback import format_exc

from bs4 import BeautifulSoup
from requests import get

from sedenbot import HELP, SEDEN_LANG
from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    google_domains,
    sedenify,
    send_log,
    useragent,
)


@sedenify(pattern='^.google')
def google(message):
    match = extract_args(message)
    if len(match) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace('page=', '')
        match = match.replace('page=' + page[0], '')
        page = int(page)
    except BaseException:
        page = 1
    msg = do_gsearch(match, page)
    edit(
        message, get_translation('googleResult', ['**', '`', match, msg]), preview=False
    )

    send_log(get_translation('googleLog', [match]))


def do_gsearch(query, page):
    def find_page(num):
        if num < 1:
            num = 1
        return (num - 1) * 10

    def parse_key(keywords):
        return keywords.replace(' ', '+')

    def replacer(st):
        return (
            sub(r'[`\*_]', '', st)
            .replace('\n', ' ')
            .replace('(', '〈')
            .replace(')', '〉')
            .replace('!', 'ⵑ')
            .strip()
        )

    def get_result(res):
        link = res.find('a', href=True)
        title = res.find('h3')
        if title:
            title = title.text
        desc = res.find(
            'div', attrs={'class': ['VwiC3b', 'yXK7lf', 'MUxGbd', 'yDYNvb', 'lyLwlc']}
        )
        if desc:
            desc = desc.text

        if link and title and desc:
            return f'[{replacer(title)}]({link["href"]})\n{desc or ""}'

    query = parse_key(query)
    page = find_page(page)
    temp = f'/search?q={query}&start={find_page(page)}&hl={SEDEN_LANG}'

    req = get(
        f'https://{choice(google_domains)}{temp}',
        headers={
            'User-Agent': useragent(),
            'Content-Type': 'text/html',
        },
    )

    retries = 0
    while req.status_code != 200 and retries < 10:
        retries += 1
        req = get(
            f'https://{choice(google_domains)}{temp}',
            headers={
                'User-Agent': useragent(),
                'Content-Type': 'text/html',
            },
        )

    soup = BeautifulSoup(req.text, 'html.parser')
    res1 = soup.find_all('div', attrs={'class': 'g'})

    out = ''
    count = 0
    for res in res1:
        try:
            result = get_result(res)
            if result:
                count += 1
                out += f'{count} - {result}\n\n'
        except Exception:
            print(format_exc())
            print(res)
            pass

    return out


HELP.update({'goolag': get_translation('googleInfo')})
