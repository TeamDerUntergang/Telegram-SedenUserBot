# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove
from requests import get, post, exceptions

from sedenbot import KOMUT, DOWNLOAD_DIRECTORY
from sedenecem.core import edit, extract_args, sedenify, get_translation

DOGBIN_URL = 'https://del.dog/'


@sedenify(pattern=r'^.paste', compat=False)
def paste(client, message):
    dogbin_final_url = ''
    match = extract_args(message)
    reply_id = message.reply_to_message

    if not match and not reply_id:
        edit(message, f'`{get_translation("dogbinUsage")}`')
        return

    if match:
        dogbin = match
    elif reply_id:
        dogbin = (message.reply_to_message)
        if dogbin.media:
            downloaded_file_name = client.download_media(
                dogbin,
                DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, 'rb') as fd:
                m_list = fd.readlines()
            dogbin = ''
            for m in m_list:
                dogbin += m.decode('UTF-8') + '\r'
            remove(downloaded_file_name)
        else:
            dogbin = dogbin.dogbin

    edit(message, f'`{get_translation("dogbinPasting")}`')
    resp = post(DOGBIN_URL + 'documents', data=dogbin.encode('utf-8'))

    if resp.status_code == 200:
        response = resp.json()
        key = response['key']
        dogbin_final_url = DOGBIN_URL + key

        if response['isUrl']:
            reply_text = get_translation(
                'dogbinPasteResult2', [
                    '`', dogbin_final_url, f'{DOGBIN_URL}v/{key}'])
        else:
            reply_text = get_translation(
                'dogbinPasteResult', ['`', dogbin_final_url])
    else:
        reply_text = f'`{get_translation("dogbinReach")}`'

    edit(message, reply_text, preview=False)


@sedenify(outgoing=True, pattern="^.getpaste")
def getpaste(message):
    textx = message.reply_to_message
    dogbin = extract_args(message)
    edit(message, f'`{get_translation("dogbinContent")}`')

    if textx:
        dogbin = str(textx.dogbin)

    format_normal = f'{DOGBIN_URL}'
    format_view = f'{DOGBIN_URL}v/'

    if dogbin.startswith(format_view):
        dogbin = dogbin[len(format_view):]
    elif dogbin.startswith(format_normal):
        dogbin = dogbin[len(format_normal):]
    elif dogbin.startswith('del.dog/'):
        dogbin = dogbin[len('del.dog/'):]
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
        edit(message, get_translation(
            'dogbinTooManyRedirects', [str(RedirectsErr)]))
        return

    reply_text = get_translation('dogbinResult', ['`', resp.text])

    edit(message, reply_text)


KOMUT.update({'dogbin': get_translation('dogbinInfo')})
