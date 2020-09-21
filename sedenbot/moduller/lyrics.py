# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from os import remove
from lyricsgenius import Genius

from sedenbot import KOMUT, GENIUS_TOKEN
from sedenecem.core import edit, reply_doc, extract_args, sedenify, get_translation


@sedenify(pattern='^.lyrics')
def lyrics(message):
    args = extract_args(message)
    if r"-" in args:
        pass
    else:
        edit(message, f'`{get_translation("lyricsError")}`')
        return

    if not GENIUS_TOKEN:
        edit(message, f'`{get_translation("geniusToken")}`')
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
            f.write(get_translation('lyricsQuery', [
                    '', '', artist, song, songs.lyrics]))
        reply_doc(message, 'lyrics.txt')
        remove('lyrics.txt')
    else:
        edit(message, get_translation('lyricsQuery', [
             '**', '`', artist, song, songs.lyrics]))
    return


KOMUT.update({"lyrics": get_translation("lyricsInfo")})
