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

from sedenbot import KOMUT
from sedenecem.core import (edit, reply, reply_img, send_log, extract_args,
                            extract_args_arr, sedenify, get_translation,
                            spam_allowed, increment_spam_count)


@sedenify(pattern='^.tspam')
def tspam(message):
    tspam = extract_args(message)
    if len(tspam) < 1:
        edit(message, f'`{get_translation("spamWrong")}`')
        return
    message.delete()

    if not spam_allowed():
        return

    for metin in tspam.replace(' ', ''):
        message.reply(metin)
        count = increment_spam_count()
        if not count:
            break

    send_log(f'{get_translation("tspamLog")}')


@sedenify(pattern='^.spam')
def spam(message):
    spam = extract_args(message)
    if len(spam) < 1:
        edit(message, f'`{get_translation("spamWrong")}`')
        return
    arr = spam.split()
    if not arr[0].isdigit():
        edit(message, f'`{get_translation("spamWrong")}`')
        return

    message.delete()

    if not spam_allowed():
        return

    miktar = int(arr[0])
    metin = spam.replace(arr[0], '', 1).strip()
    for i in range(0, miktar):
        reply(message, metin)
        count = increment_spam_count()
        if not count:
            break

    send_log(f'{get_translation("spamLog")}')


@sedenify(pattern='^.picspam')
def picspam(message):
    arr = extract_args_arr(message)
    if len(arr) < 2 or not arr[0].isdigit():
        edit(message, f'`{get_translation("spamWrong")}`')
        return
    message.delete()

    if not spam_allowed():
        return

    miktar = int(arr[0])
    link = arr[1]
    for i in range(0, miktar):
        reply_img(message, link)
        count = increment_spam_count()
        if not count:
            break

    send_log(f'{get_translation("picspamLog")}')


@sedenify(pattern='^.delayspam')
def delayspam(message):
    """Copyright (c) @ReversedPosix | 2020"""
    delayspam = extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        edit(message, f'`{get_translation("spamWrong")}`')
        return
    gecikme = int(arr[0])
    miktar = int(arr[1])
    spam_message = delayspam.replace(arr[0], '', 1)
    spam_message = spam_message.replace(arr[1], '', 1).strip()
    message.delete()

    if not spam_allowed():
        return

    delaySpamEvent = Event()
    for i in range(0, miktar):
        if i != 0:
            delaySpamEvent.wait(gecikme)
        message.reply(spam_message)
        count = increment_spam_count()
        if not count:
            break

    send_log(f'{get_translation("delayspamLog")}')


KOMUT.update({"spammer": get_translation('spamInfo')})
