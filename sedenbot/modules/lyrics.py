# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from lyricsgenius import Genius
from sedenbot import GENIUS_TOKEN, HELP
from sedenecem.core import edit, extract_args, get_translation, reply_doc, sedenify


@sedenify(pattern='^.lyrics')
def lyrics(message):
    args = extract_args(message)
    if r'-' in args:
        pass
    else:
        return edit(message, f'`{get_translation("lyricsError")}`')

    if not GENIUS_TOKEN:
        return edit(message, f'`{get_translation("geniusToken")}`')
    else:
        genius = Genius(GENIUS_TOKEN)
        try:
            args = args.split('-')
            artist = args[0].strip()
            song = args[1].strip()
        except BaseException:
            edit(message, f'`{get_translation("lyricsError2")}`')
            return

    if len(args) < 1:
        edit(message, f'`{get_translation("lyricsError2")}`')
        return

    edit(message, get_translation('lyricsSearch', ['`', artist, song]))

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if not songs:
        edit(message, get_translation('lyricsNotFound', ['**', artist, song]))
        return
    if len(songs.lyrics) > 4096:
        edit(message, f'`{get_translation("lyricsOutput")}`')
        with open('lyrics.txt', 'w+') as f:
            f.write(
                get_translation('lyricsQuery', ['', '', artist, song, songs.lyrics])
            )
        reply_doc(message, 'lyrics.txt', delete_after_send=True)
    else:
        edit(
            message,
            get_translation('lyricsQuery', ['**', '`', artist, song, songs.lyrics]),
        )
    return


HELP.update({'lyrics': get_translation('lyricsInfo')})
