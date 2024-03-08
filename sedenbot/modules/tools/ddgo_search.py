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
from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    sedenify,
    send_log,
    useragent,
)


@sedenify(pattern='^.d(uckduck|d)go')
def ddgo(message):
    query = extract_args(message)
    if len(query) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    req = get(
        f'https://duckduckgo.com/lite?q={query}',
        headers={
            'User-Agent': useragent(),
            'Content-Type': 'text/html',
        },
    )
    soup = BeautifulSoup(req.text, 'html.parser')
    res1 = soup.findAll('table', {'border': 0})
    res1 = res1[-1].findAll('tr')

    match = do_ddsearch(res1)
    edit(
        message,
        get_translation('googleResult', ['**', '`', query, match]),
        preview=False,
    )
    send_log(get_translation('ddgoLog', [query]))


def do_ddsearch(res1):
    def splitter(res):
        subs = []
        tlist = None
        comp = False
        for i in range(len(res)):
            item = res[i]
            if res3 := item.find('a', {'class': ['result-link']}):
                if comp:
                    subs.append(tlist)
                comp = True
                tlist = []
                tlist.append(res3)
            elif res4 := item.find('td', {'class': ['result-snippet']}):
                tlist.append(res4)
                subs.append(tlist)
            if len(subs) > 9:
                break
        return subs

    res1 = splitter(res1)

    out = ''
    for i in range(len(res1)):
        item = res1[i]
        link = item[0]
        ltxt = link.text.replace('|', '-').replace('...', '').strip()
        desc = item[1].text.strip() if len(item) > 1 else get_translation('ddgoDesc')
        out += f'{i+1} - [{ltxt}]({link["href"]})\n{desc}\n\n'

    return out


HELP.update({'duckduckgo': get_translation('ddgoInfo')})
