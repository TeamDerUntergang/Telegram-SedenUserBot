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

from threading import Event
from re import sub

from sedenbot import KOMUT
from sedenecem.core import (edit, reply, reply_img, send_log, extract_args,
                            extract_args_arr, sedenify)

@sedenify(pattern='^.tspam')
def tspam(message):
    tspam = extract_args(message)
    if len(tspam) < 1:
        edit(message, '`Bir şeyler eksik/yanlış gibi görünüyor.`')
        return
    message.delete()
    for metin in tspam.replace(' ', ''):
        message.reply(metin)

    send_log('#TSPAM \n'
             'TSpam başarıyla gerçekleştirildi')

@sedenify(pattern='^.spam')
def spam(message):
    spam = extract_args(message)
    if len(spam) < 1:
        edit(message, '`Bir şeyler eksik/yanlış gibi görünüyor.`')
        return
    arr = spam.split()
    if not arr[0].isdigit():
        edit(message, '`Bir şeyler eksik/yanlış gibi görünüyor.`')
        return
    message.delete()
    miktar = int(arr[0])
    metin = spam.replace(arr[0], '').strip()
    for i in range(0, miktar):
        reply(message, metin)

    send_log('#SPAM \n'
             'Spam başarıyla gerçekleştirildi')

@sedenify(pattern='^.picspam')
def picspam(message):
    arr = extract_args_arr(message)
    if len(arr) < 2 or not arr[0].isdigit():
        edit(message, '`Bir şeyler eksik/yanlış gibi görünüyor.`')
        return
    message.delete()
    miktar = int(arr[0])
    link = arr[1]
    for i in range(0, miktar):
        reply_img(message, link)

    send_log('#PICSPAM \n'
             'PicSpam başarıyla gerçekleştirildi')

# Copyright (c) @ReversedPosix | 2020
@sedenify(pattern='^.delayspam')
def delayspam(message):
    delayspam = extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        edit(message, '`Bir şeyler eksik/yanlış gibi görünüyor.`')
        return
    gecikme = int(arr[0])
    miktar = int(arr[1])
    spam_message = sub(f'{arr[0]}|{arr[1]}', '', delayspam).strip()
    message.delete()
    delaySpamEvent = Event()
    for i in range(0, miktar):
        message.reply(spam_message)
        delaySpamEvent.wait(gecikme)

    send_log('#DELAYSPAM \n'
             'DelaySpam başarıyla gerçekleştirildi')

KOMUT.update({
    "spammer": ".tspam <metin>\
\nKullanım: Verilen mesajı tek tek göndererek spam yapar\
\n\n.spam <miktar> <metin>\
\nKullanım: Verilen miktarda spam gönderir\
\n\n.picspam <miktar> <link>\
\nKullanım: Verilen miktarda resimli spam gönderir\
\n\n.delayspam <gecikme> <miktar> <metin>\
\nKullanım: Verilen miktar ve verilen gecikme ile gecikmeli spam yapar\
\n\n\nNOT : Sorumluluk size aittir!!"
})
