# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import JSONDecodeError, loads

from requests import RequestException, get

from sedenbot import HELP, SEDEN_LANG
from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    reply_doc,
    sedenify,
    send_log,
)


@sedenify(pattern='^.wiki')
def wiki(message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    try:
        result = search_wiki(args)
    except BaseException as e:
        raise e

    if len(result) > 4096:
        with open(f'{args}.txt', 'w', encoding='utf-8') as file:
            file.write(result)
        return reply_doc(
            message,
            f'{args}.txt',
            caption=f'`{get_translation("outputTooLarge")}`',
            delete_after_send=True,
        )

    edit(message, get_translation('sedenQuery', ['**', '`', args, result]))
    send_log(get_translation('wikiLog', ['`', args]))


def search_wiki(query):
    url = f'https://{SEDEN_LANG or "en"}.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'titles': query,
        'exsectionformat': 'wiki',
        'explaintext': 1,
    }

    try:
        response = get(url, params=params)
        response.raise_for_status()
        data = loads(response.text)
        pages = data.get('query', {}).get('pages', {})
        result = ''

        for page in pages.values():
            extract = page.get('extract', '')
            result += extract

        if not result:
            result = get_translation('wikiError')

        return result

    except (RequestException, JSONDecodeError) as e:
        print(f'API Error: {e}')
        return ''


HELP.update({'wiki': get_translation('wikiInfo')})
