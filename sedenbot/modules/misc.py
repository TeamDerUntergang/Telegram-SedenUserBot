# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove
from random import choice
from subprocess import PIPE
from subprocess import run as runapp

from image_to_ascii import ImageToAscii
from pybase64 import b64decode, b64encode
from sedenbot import HELP, SUPPORT_GROUP
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_translation,
    reply,
    reply_doc,
    sedenify,
)


@sedenify(pattern='^.random')
def random(message):
    items = extract_args(message, False)
    args = items.split()
    if len(args) < 2:
        edit(message, f'`{get_translation("randomUsage")}`')
        return

    edit(message, get_translation('randomResult', ['**', '`', items, choice(args)]))


@sedenify(pattern='^.chatid$', private=False)
def chatid(message):
    edit(message, get_translation('chatidResult', ['`', str(message.chat.id)]))


@sedenify(pattern='^.invitelink$', compat=False, admin=True, private=False)
def get_invite_link(client, message):
    chat = client.get_chat(message.chat.id)
    try:
        url = chat.invite_link
        edit(message, url, preview=False)
    except BaseException:
        pass


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
        edit(message, get_translation('useridResult', ['**', name, '`', user_id]))
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')


@sedenify(pattern='^.kickme$', compat=False, private=False)
def kickme(client, message):
    edit(message, f'`{get_translation("kickmeResult")}`')
    client.leave_chat(message.chat.id, 'me')


@sedenify(pattern='^.support$')
def support(message):
    edit(message, get_translation('supportResult', [SUPPORT_GROUP]), preview=False)


@sedenify(pattern='^.founder')
def founder(message):
    edit(message, get_translation('founderResult', ['`', '**']), preview=False)


@sedenify(pattern='^.readme$')
def readme(message):
    edit(
        message,
        '[Seden README.md](https://github.com/TeamDerUntergang/'
        'Telegram-SedenUserBot/blob/seden/README.md)',
        preview=False,
    )


@sedenify(pattern='^.repo$')
def repo(message):
    edit(
        message,
        '[Seden Repo](https://github.com/TeamDerUntergang/' 'Telegram-SedenUserBot)',
        preview=False,
    )


@sedenify(pattern='^.repeat')
def repeat(message):
    # Copyright (c) Gegham Zakaryan | 2019
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

    replyText = f'{toBeRepeated}\n'

    for i in range(0, replyCount - 1):
        replyText += f'{toBeRepeated}\n'

    edit(message, replyText)


@sedenify(pattern='^.crash$')
def crash(message):
    edit(message, f'`{get_translation("testLogId")}`')
    raise Exception(get_translation('testException'))


@sedenify(pattern='^.tagall$', compat=False, private=False)
def tagall(client, message):
    msg = '@tag'
    chat = message.chat.id
    length = 0
    for member in client.iter_chat_members(chat):
        if length < 4092:
            msg += f'[\u2063](tg://user?id={member.user.id})'
            length += 1
    reply(message, msg, delete_orig=True)


@sedenify(pattern='^.report$', compat=False, private=False)
def report_admin(client, message):
    msg = '@admin'
    chat = message.chat.id
    for member in client.iter_chat_members(chat, filter='administrators'):
        msg += f'[\u2063](tg://user?id={member.user.id})'
    re_msg = message.reply_to_message
    reply(re_msg if re_msg else message, msg)
    message.delete()


@sedenify(pattern='^.hash')
def hash(message):
    hashtxt_ = extract_args(message)
    if len(hashtxt_) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    hashtxt = open('hash.txt', 'w+')
    hashtxt.write(hashtxt_)
    hashtxt.close()
    md5 = runapp(['md5sum', 'hash.txt'], stdout=PIPE)
    md5 = md5.stdout.decode()
    sha1 = runapp(['sha1sum', 'hash.txt'], stdout=PIPE)
    sha1 = sha1.stdout.decode()
    sha256 = runapp(['sha256sum', 'hash.txt'], stdout=PIPE)
    sha256 = sha256.stdout.decode()
    sha512 = runapp(['sha512sum', 'hash.txt'], stdout=PIPE)
    runapp(['rm', 'hash.txt'], stdout=PIPE)
    sha512 = sha512.stdout.decode()

    def rem_filename(st):
        return st[: st.find(' ')]

    ans = (
        f'Text: `{hashtxt_}`'
        f'\nMD5: `{rem_filename(md5)}`'
        f'\nSHA1: `{rem_filename(sha1)}`'
        f'\nSHA256: `{rem_filename(sha256)}`'
        f'\nSHA512: `{rem_filename(sha512)}`'
    )
    if len(ans) > 4096:
        hashfile = open('hash.txt', 'w+')
        hashfile.write(ans)
        hashfile.close()
        reply_doc(message, 'hash.txt', caption=f'`{get_translation("outputTooLarge")}`')
        runapp(['rm', 'hash.txt'], stdout=PIPE)
        message.delete()
    else:
        edit(message, ans)


@sedenify(pattern='^.base64')
def base64(message):
    argv = extract_args(message)
    args = argv.split(' ', 1)
    if len(args) < 2 or args[0] not in ['en', 'de']:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    args[1] = args[1].replace('`', '')
    if args[0] == 'en':
        lething = str(b64encode(bytes(args[1], 'utf-8')))[2:]
        edit(message, f'Input: `{args[1]}`\nEncoded: `{lething[:-1]}`')
    else:
        lething = str(b64decode(bytes(args[1], 'utf-8')))[2:]
        edit(message, f'Input: `{args[1]}`\nDecoded: `{lething[:-1]}`')


@sedenify(pattern='^.ascii$')
def img_to_ascii(message):
    reply = message.reply_to_message
    edit(message, f'`{get_translation("processing")}`')
    if not reply:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    if not (
        reply.photo
        or (reply.sticker and not reply.sticker.is_animated)
        or (reply.document and 'image' in reply.document.mime_type)
    ):
        edit(message, f'`{get_translation("wrongMedia")}`')
    else:
        media = download_media_wc(reply, file_name='ascii.png')
        ImageToAscii(imagePath=media, outputFile="output.txt")
        reply_doc(reply, 'output.txt', delete_after_send=True)
        message.delete()
        remove(media)


HELP.update({'misc': get_translation('miscInfo')})
