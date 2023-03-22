# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from requests import get, post
from requests.exceptions import HTTPError, Timeout, TooManyRedirects

from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, sedenify


@sedenify(pattern='^.paste')
def pastebin(message):
    paste = extract_args(message, line=False)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("processing")}`')

    url = "https://dpaste.org/api/"

    if reply:
        if not reply.text:
            return edit(message, f'`{get_translation("pasteErr")}`')
        paste = reply.text

    try:
        r = post(
            url=url,
            data={
                'content': paste.encode('utf-8'),
                'lexer': '_text',
                'expires': '3600',
            },
        )
    except BaseException as e:
        raise e

    try:
        resp = r.text
        out = resp.replace('"', '')
        return edit(message, out, preview=False)
    except BaseException as e:
        raise e


@sedenify(pattern='^.getpaste')
def get_hastebin_text(message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("processing")}`')

    if reply:
        args = reply.text

    if args.startswith('https://dpaste.org/'):
        args = args[len('https://dpaste.org/') :]
    elif args.startswith('dpaste.org/'):
        args = args[len('dpaste.org/') :]
    else:
        return edit(message, f'`{get_translation("wrongURL")}`')

    resp = get(f'https://dpaste.org/{args}/raw')

    try:
        resp.raise_for_status()
    except HTTPError as err:
        return edit(message, get_translation('banError', ['`', '**', err]))
    except Timeout as err:
        return edit(message, get_translation('banError', ['`', '**', err]))
    except TooManyRedirects as err:
        return edit(message, get_translation('banError', ['`', '**', err]))

    edit(message, get_translation('getPasteOut', ['`', resp.text]))


HELP.update({'pastebin': get_translation('pasteInfo')})
