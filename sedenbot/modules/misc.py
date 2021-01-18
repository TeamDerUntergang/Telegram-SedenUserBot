# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from random import choice

from sedenbot import HELP, SUPPORT_GROUP
from sedenecem.core import edit, extract_args, sedenify, get_translation


@sedenify(pattern='^.random')
def random(message):
    items = extract_args(message, False)
    args = items.split()
    if len(args) < 2:
        edit(message, f'`{get_translation("randomUsage")}`')
        return

    edit(message, get_translation(
        'randomResult', ['**', '`', items, choice(args)]))


@sedenify(pattern='^.chatid$', private=False)
def chatid(message):
    edit(
        message,
        get_translation('chatidResult', ['`', str(message.chat.id)]))


@sedenify(pattern='^.id$')
def userid(message):
    reply = message.reply_to_message
    if reply:
        if not reply.forward_from:
            user_id = reply.from_user.id
            if reply.from_user.username:
                name = f'**@{reply.from_user.username}**'
            else:
                name = f'**[{reply.from_user.first_name}](tg://user?id={reply.from_user.id})**'
        else:
            user_id = reply.forward_from.id
            if reply.forward_from.username:
                name = f'**@{reply.forward_from.username}**'
            else:
                name = f'**[{reply.forward_from.first_name}](tg://user?id={reply.forward_from.id})**'
        edit(
            message, get_translation(
                'useridResult', [
                    '**', name, '`', user_id]))
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')


@sedenify(pattern='^.kickme$', compat=False, private=False)
def kickme(client, message):
    edit(message, f'`{get_translation("kickmeResult")}`')
    client.leave_chat(message.chat.id, 'me')


@sedenify(pattern='^.support$')
def support(message):
    edit(message, get_translation('supportResult', [SUPPORT_GROUP]),
         preview=False)


@sedenify(pattern='^.founder')
def founder(message):
    edit(message, get_translation('founderResult', ['`', '**']), preview=False)


@sedenify(pattern='^.readme$')
def readme(message):
    edit(
        message,
        '[Seden README.md](https://github.com/TeamDerUntergang/'
        'Telegram-SedenUserBot/blob/seden/README.md)',
        preview=False)


@sedenify(pattern='^.repo$')
def repo(message):
    edit(
        message,
        '[Seden Repo](https://github.com/TeamDerUntergang/'
        'Telegram-SedenUserBot)',
        preview=False)


@sedenify(pattern='^.repeat')
def repeat(message):
    '''Copyright (c) Gegham Zakaryan | 2019'''
    args = extract_args(message).split(' ', 1)
    if len(args) < 2:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    cnt, txt = args
    if not cnt.isdigit():
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + '\n'

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + '\n'

    edit(message, replyText)


@sedenify(pattern='^.crash$')
def crash(message):
    edit(message, f'`{get_translation("testLogId")}`')
    raise Exception(get_translation('testException'))


HELP.update({'misc': get_translation('miscInfo')})
