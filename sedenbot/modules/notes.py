# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from sedenbot import HELP, LOG_ID, LOGS
from sedenecem.core import (
    edit,
    extract_args,
    forward,
    get_messages,
    get_translation,
    reply_msg,
    sedenify,
    send_log,
)


def notes_init():
    try:
        global sql
        from importlib import import_module

        sql = import_module('sedenecem.sql.notes_sql')
    except Exception as e:
        sql = None
        LOGS.warn(get_translation('notesSqlLog'))
        raise e


notes_init()


@sedenify(pattern='^.notes$')
def notes(message):
    try:
        from sedenecem.sql.notes_sql import get_notes
    except AttributeError:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    reply = f'`{get_translation("noNote")}`'
    notesx = get_notes(message.chat.id)
    for note in notesx:
        if reply == f'`{get_translation("noNote")}`':
            reply = f'{get_translation("notesChats")}\n'
            reply += '`#{}`\n'.format(note.keyword)
        else:
            reply += '`#{}`\n'.format(note.keyword)
    edit(message, reply)


@sedenify(pattern=r'^.save')
def save_note(message):
    try:
        from sedenecem.sql.notes_sql import add_note
    except AttributeError:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    args = extract_args(message, markdown=True).split(' ', 1)
    if len(args) < 1 or len(args[0]) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    keyword = args[0]
    string = args[1] if len(args) > 1 else ''
    msg = message.reply_to_message
    msg_id = None

    if len(string) < 1:
        if msg:
            if msg.text:
                string = msg.text.markdown
            else:
                string = None
                msg_o = forward(msg, LOG_ID)
                if not msg_o:
                    edit(message, f'`{get_translation("noteError")}`')
                    return
                msg_id = msg_o.message_id
                send_log(get_translation('notesLog', ['`', message.chat.id, keyword]))
        else:
            edit(message, f'`{get_translation("wrongCommand")}`')

    if add_note(str(message.chat.id), keyword, string, msg_id) is False:
        edit(message, get_translation('notesUpdated', ['`', keyword]))
    else:
        edit(message, get_translation('notesAdded', ['`', keyword]))


@sedenify(pattern=r'^.clear')
def clear_note(message):
    try:
        from sedenecem.sql.notes_sql import rm_note
    except AttributeError:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    notename = extract_args(message)
    if rm_note(message.chat.id, notename) is False:
        edit(message, get_translation('notesNotFound', ['`', notename]))
    else:
        edit(message, get_translation('notesRemoved', ['**', '`', notename]))


def get_note(message):
    try:
        try:
            from sedenecem.sql.notes_sql import get_note
        except BaseException:
            edit(message, f'`{get_translation("nonSqlMode")}`')
            return

        notename = extract_args(message).split()[0][1:]
        note = get_note(message.chat.id, notename)

        if note:
            if note.f_mesg_id:
                msg_o = get_messages(LOG_ID, msg_ids=int(note.f_mesg_id))
                if msg_o and len(msg_o) > 0 and not msg_o[-1].empty:
                    msg = msg_o[-1]
                    reply_msg(message, msg)
                else:
                    edit(message, f'`{get_translation("noteResult")}`')
            elif note.reply and len(note.reply) > 0:
                edit(message, note.reply)
            else:
                edit(message, f'`{get_translation("noteError2")}`')
        else:
            edit(message, f'`{get_translation("noteNoFound")}`')
    except BaseException:
        pass


HELP.update({'notes': get_translation('notesInfo')})
