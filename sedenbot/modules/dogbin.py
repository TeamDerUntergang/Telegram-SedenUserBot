# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from requests import exceptions, get, post
from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, sedenify

DOGBIN_URL = 'https://del.dog/'


@sedenify(pattern='^.paste')
def paste(message):
    match = extract_args(message)
    reply = message.reply_to_message

    if match:
        pass
    elif reply:
        if not reply.text:
            return edit(message, f'`{get_translation("dogbinUsage")}`')
        match = reply.text
    else:
        edit(message, f'`{get_translation("dogbinUsage")}`')
        return

    edit(message, f'`{get_translation("dogbinPasting")}`')
    resp = post(f'{DOGBIN_URL}documents', data=match.encode('utf-8'))

    dogbin_final_url = ''
    if resp.status_code == 200:
        response = resp.json()
        key = response['key']
        dogbin_final_url = f'{DOGBIN_URL}{key}'

        if response['isUrl']:
            reply_text = get_translation(
                'dogbinPasteResult2', ['`', dogbin_final_url, f'{DOGBIN_URL}v/{key}']
            )
        else:
            reply_text = get_translation('dogbinPasteResult', ['`', dogbin_final_url])
    else:
        reply_text = f'`{get_translation("dogbinReach")}`'

    edit(message, reply_text, preview=False)


@sedenify(outgoing=True, pattern="^.getpaste")
def getpaste(message):
    reply = message.reply_to_message
    match = extract_args(message)
    edit(message, f'`{get_translation("dogbinContent")}`')

    if reply:
        match = str(reply.text)

    format_normal = f'{DOGBIN_URL}'
    format_view = f'{DOGBIN_URL}v/'

    if match.startswith(format_view):
        dogbin = match[len(format_view) :]
    elif match.startswith(format_normal):
        dogbin = match[len(format_normal) :]
    elif match.startswith('del.dog/'):
        dogbin = match[len('del.dog/') :]
    else:
        edit(message, f'`{get_translation("dogbinUrlError")}`')
        return

    resp = get(f'{DOGBIN_URL}raw/{dogbin}')

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        edit(message, get_translation('dogbinError', [str(HTTPErr)]))
        return
    except exceptions.Timeout as TimeoutErr:
        edit(message, get_translation('dogbinTimeOut', [str(TimeoutErr)]))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        edit(message, get_translation('dogbinTooManyRedirects', [str(RedirectsErr)]))
        return

    reply_text = get_translation('dogbinResult', ['`', resp.text])

    edit(message, reply_text, preview=False)


HELP.update({'dogbin': get_translation('dogbinInfo')})
