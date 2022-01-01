# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from threading import Event

from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args,
    extract_args_arr,
    get_translation,
    increment_spam_count,
    reply,
    reply_img,
    sedenify,
    send_log,
    spam_allowed,
)


@sedenify(pattern='^.tspam')
def tspam(message):
    tspam = extract_args(message)
    if len(tspam) < 1:
        edit(message, f'`{get_translation("spamWrong")}`')
        return
    message.delete()

    if not spam_allowed():
        return

    for text in tspam.replace(' ', ''):
        reply(message, text)
        count = increment_spam_count()
        if not count:
            break

    send_log(get_translation('tspamLog'))


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

    count = int(arr[0])
    text = spam.replace(arr[0], '', 1).strip()
    for i in range(0, count):
        reply(message, text)
        limit = increment_spam_count()
        if not limit:
            break

    send_log(get_translation('spamLog'))


@sedenify(pattern='^.picspam')
def picspam(message):
    arr = extract_args_arr(message)
    if len(arr) < 2 or not arr[0].isdigit():
        edit(message, f'`{get_translation("spamWrong")}`')
        return
    message.delete()

    if not spam_allowed():
        return

    count = int(arr[0])
    url = arr[1]
    for i in range(0, count):
        reply_img(message, url)
        limit = increment_spam_count()
        if not limit:
            break

    send_log(get_translation('picspamLog'))


@sedenify(pattern='^.delayspam')
def delayspam(message):
    # Copyright (c) @ReversedPosix | 2020-2021
    delayspam = extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        edit(message, f'`{get_translation("spamWrong")}`')
        return
    delay = int(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], '', 1)
    spam_message = spam_message.replace(arr[1], '', 1).strip()
    message.delete()

    if not spam_allowed():
        return

    delaySpamEvent = Event()
    for i in range(0, count):
        if i != 0:
            delaySpamEvent.wait(delay)
        reply(message, spam_message)
        limit = increment_spam_count()
        if not limit:
            break

    send_log(get_translation('delayspamLog'))


HELP.update({'spammer': get_translation('spamInfo')})
