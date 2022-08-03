# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
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


@sedenify(pattern="^.paste")
def paste_hastebin(message):
    text = message.text.strip()
    reply = message.reply_to_message
    edit(message, f'`{get_translation("processing")}`')
    if not reply and len(text) <= 6:
        return edit(message, f'`{get_translation("pasteErr")}`')

    paste = text.replace('.paste ', '')
    url = "https://hastebin.com/documents"

    if reply:
        if not reply.text:
            return edit(message, f'`{get_translation("pasteErr")}`')
        paste = reply.text

    try:
        r = post(
            url=url,
            data=paste.encode('utf-8'),
        )
    except BaseException as e:
        edit(message, f'`{get_translation("pasteConErr")}`')

    try:
        resp = r.json()
        key = resp['key']
        new_url = f"https://hastebin.com/{key}"
        return edit(message, new_url, preview=False)
    except BaseException as e:
        raise e


@sedenify(pattern='^.getpaste')
def get_hastebin_text(message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("processing")}`')

    if reply:
        args = reply.text

    if args.startswith('https://hastebin.com/'):
        args = args[len('https://hastebin.com/') :]
    elif args.startswith("hastebin.com/"):
        args = args[len("hastebin.com/") :]
    else:
        return edit(message, f'`{get_translation("wrongURL")}`')

    resp = get(f'https://hastebin.com/raw/{args}')

    try:
        resp.raise_for_status()
    except HTTPError as err:
        return edit(message, get_translation('banError', ['`', '**', err]))
    except Timeout as err:
        return edit(message, get_translation('banError', ['`', '**', err]))
    except TooManyRedirects as err:
        return edit(message, get_translation('banError', ['`', '**', err]))

    out = f'`Hastebin içeriği başarıyla getirildi!`\n\n`İçerik:` {resp.text}'

    edit(message, out)


HELP.update({'hastebin': get_translation('pasteInfo')})
