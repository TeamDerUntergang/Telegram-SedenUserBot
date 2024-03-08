# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep

from sedenbot import HELP, LOGS
from sedenecem.core import edit, extract_args, get_translation, sedenify, send_log


def chat_init():
    try:
        global sql
        from importlib import import_module

        sql = import_module('sedenecem.sql.keep_read_sql')
    except Exception as e:
        sql = None
        LOGS.warn(get_translation('chatSqlLog'))
        raise e


chat_init()


@sedenify(pattern='^.unmutechat$')
def unmutechat(message):
    try:
        from sedenecem.sql.keep_read_sql import unkread
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    status = unkread(str(message.chat.id))
    if status:
        edit(message, f'`{get_translation("chatUnmuted")}`')
    else:
        edit(message, f'`{get_translation("chatAlreadyUnmuted")}`')
    sleep(2)
    message.delete()


@sedenify(pattern='^.mutechat$')
def mutechat(message):
    try:
        from sedenecem.sql.keep_read_sql import kread
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    status = kread(str(message.chat.id))
    if status:
        edit(message, f'`{get_translation("chatMuted")}`')
    else:
        edit(message, f'`{get_translation("chatAlreadyMuted")}`')
    sleep(2)
    message.delete()

    send_log(get_translation('chatLog', [message.chat.id]))


@sedenify(incoming=True, outgoing=False)
def keep_read(message):
    if message.from_user and message.from_user.is_self:
        message.continue_propagation()

    try:
        from sedenecem.sql.keep_read_sql import is_kread
    except BaseException:
        message.continue_propagation()

    if is_muted(message.chat.id):
        message._client.read_chat_history(message.chat.id)

    message.continue_propagation()


@sedenify(pattern='^.call')
def call_notes(message):
    try:
        from sedenbot.modules.deneme.notes import get_note
        from sedenbot.modules.var.snips import get_snip
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    args = extract_args(message)
    if args.startswith('#'):
        get_note(message)
    elif args.startswith('$'):
        get_snip(message)
    else:
        edit(message, f"`{get_translation('wrongCommand')}`")


def is_muted(chat_id):
    try:
        from sedenecem.sql.keep_read_sql import is_kread
    except BaseException:
        return False

    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(chat_id):
                return True

    return False


HELP.update({'chat': get_translation('chatInfo')})
HELP.update({'call': get_translation('callInfo')})
