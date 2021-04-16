# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from deethon import Session
from sedenbot import DEEZER_TOKEN, HELP
from sedenecem.core import edit, extract_args, get_translation, reply_audio, sedenify


@sedenify(pattern='^.deezer')
def deezermusic(message):
    if not DEEZER_TOKEN:
        return edit(message, f'`{get_translation("deezerArlMissing")}`')
    args = extract_args(message)
    url = args
    edit(message, f'`{get_translation("processing")}`')
    if not url:
        return edit(message, f'`{get_translation("wrongCommand")}`')

    try:
        deezer = Session(DEEZER_TOKEN)
    except Exception as e:
        return edit(message, get_translation('banError', ['`', '**', e]))

    try:
        if 'deezer' in url:
            if 'track' in url:
                track = deezer.download(url, bitrate='MP3_320')
                edit(message, f'`{get_translation("uploadMedia")}`')
                reply_audio(message, track, delete_orig=True)
            elif 'album' in url:
                album = deezer.download(url, bitrate='MP3_320')
                edit(message, f'`{get_translation("uploadMedia")}`')
                for track in album:
                    reply_audio(message, track, delete_orig=True)
    except Exception as e:
        return edit(message, get_translation('banError', ['`', '**', e]))


HELP.update({'deezer': get_translation('deezerInfo')})
