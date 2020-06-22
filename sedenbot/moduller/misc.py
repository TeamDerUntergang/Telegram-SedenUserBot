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

from random import choice

from sedenbot import KOMUT, SUPPORT_GROUP
from sedenecem.events import edit, extract_args, sedenify

@sedenify(pattern='^.random')
def random(message):
    items = extract_args(message, False)
    args = items.split()
    if len(args) < 2:
        edit(message, '`2 veya daha fazla seçenek gerekli.`')
        return

    edit(message, f'**Sorgu:**\n`{items}`\n**Çıktı:**\n`{choice(args)}`')

@sedenify(pattern='^.support$')
def support(message):
    edit(message, f'[Buradan](http://t.me/{SUPPORT_GROUP}) destek grubumuza ulaşabilirsiniz.', preview=False)

@sedenify(pattern='^.founder')
def founder(message):
    edit(message, '`=======================================`\n\n'
                 '`Bu bot;`\n'
                 '[NaytSeyd](https://t.me/NightShade) `ve` [frknkrc44](https://t.me/KaldirimMuhendisi) `tarafından geliştirilmektedir.`\n'
                 '`Ek olarak`\n'
                 '[Sedenogen](https://t.me/CiyanogenOneTeams) `tarafından sevgi ile düzenlenmiştir.`\n\n'
                 '`=======================================`', preview=False)

@sedenify(pattern='^.readme$')
def readme(message):
    edit(message, "[Seden README.md](https://github.com/TeamDerUntergang/Telegram-SedenUserBot/blob/seden/README.md)", preview=False)

@sedenify(pattern='^.repo$')
def repo(message):
    edit(message, "[Seden Repo](https://github.com/TeamDerUntergang/Telegram-SedenUserBot)", preview=False)

@sedenify(pattern='^.repeat')
# Copyright (c) Gegham Zakaryan | 2019
def repeat(message):
    args = extract_args(message).split(' ', 1)
    if len(args) < 2:
        edit(message, '`Kullanım şekli hatalı.`')
        return
    cnt, txt = args
    if not cnt.isdigit():
        edit(message, '`Kullanım şekli hatalı.`')
        return
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    edit(message, replyText)

@sedenify(pattern='^.crash$')
def crash(message):
    edit(message, '`LOG_ID değeri test ediliyor ...`')
    raise Exception('Bu bir test, hata kaydı göndermeyin.')


KOMUT.update({
    'random':
    '.random <eşya1> <eşya2> ... <eşyaN>\
\nKullanım: Eşya listesinden rastgele bir eşya seçer'
})

KOMUT.update({
    'support':
    ".support\
\nKullanım: Yardıma ihtiyacın olursa bu komutu kullan."
})

KOMUT.update({
    'repo':
    '.repo\
\nKullanım: Seden UserBot GitHub reposu'
})

KOMUT.update({
    "readme":
    ".readme\
\nKullanım: Seden botunun GitHub'daki README.md dosyasına giden bir bağlantı."
})

KOMUT.update({
    "founder":
    ".founder\
\nKullanım: Bu güzel botu kimlerin oluşturduğunu öğren :-)"
})

KOMUT.update({
    "repeat":
    ".repeat <sayı> <metin>\
\nKullanım: Bir metni belli bir sayıda tekrar eder. Spam komutu ile karıştırma!"
})
