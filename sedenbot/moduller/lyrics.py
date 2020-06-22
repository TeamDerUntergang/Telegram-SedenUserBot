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

import os
import lyricsgenius

from sedenbot import KOMUT, GENIUS_TOKEN
from sedenecem.events import edit, reply_doc, extract_args, sedenify

@sedenify(pattern='^.lyrics')
def lyrics(message):
    args = extract_args(message)
    if r"-" in args:
        pass
    else:
        edit(message, "`Hata: lütfen <sanatçı> ve <şarkı> için bölücü olarak '-' kullanın`\n"
                     "`Örnek: Rota - Belki Başka Zaman`")
        return

    if not GENIUS_TOKEN:
        edit(message,
            '`Lütfen Genius tokeni ayarlayınız. Teşekkürler!`')
    else:
        genius = lyricsgenius.Genius(GENIUS_TOKEN)
        try:
            args = args.split('-')
            artist = args[0].strip()
            song = args[1].strip()
        except:
            edit(message, '`Lütfen sanatçı ve şarkı ismini veriniz`')
            return

    if len(args) < 1:
        edit(message, '`Lütfen sanatçı ve şarkı ismini veriniz`')
        return

    edit(message, f'`{artist} - {song} için şarkı sözleri aranıyor...`')

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if not songs:
        edit(message, f'Şarkı **{artist} - {song}** bulunamadı!')
        return
    if len(songs.lyrics) > 4096:
        edit(message, '`Şarkı sözleri çok uzun, görmek için dosyayı görüntüleyin.`')
        with open('lyrics.txt', 'w+') as f:
            f.write(f'Arama sorgusu: \n{artist} - {song}\n\n{songs.lyrics}')
        reply_doc(message, 'lyrics.txt')
        os.remove('lyrics.txt')
    else:
        edit(message, f'**Arama sorgusu**: \n`{artist} - {song}`\n\n```{songs.lyrics}```')
    return

KOMUT.update({
    "lyrics":
    "Kullanım: .`lyrics <sanatçı adı> - <şarkı ismi>`\n"
    "NOT: ""-"" ayracı önemli!"
})
