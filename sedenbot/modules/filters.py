# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from re import IGNORECASE, fullmatch

from sedenbot import HELP, LOG_ID, LOGS
from sedenecem.core import (
    edit,
    extract_args,
    forward,
    get_messages,
    get_translation,
    reply,
    reply_msg,
    sedenify,
    send_log,
)


def filters_init():
    try:
        global sql
        from importlib import import_module

        sql = import_module('sedenecem.sql.filters_sql')
    except Exception as e:
        sql = None
        LOGS.warn(get_translation('filtersSqlLog'))
        raise e


filters_init()


@sedenify(incoming=True, outgoing=False)
def filter_incoming(message):
    if message.from_user and message.from_user.is_self:
        message.continue_propagation()

    name = message.text
    if not name:
        message.continue_propagation()

    try:
        from sedenecem.sql.filters_sql import get_filters
    except BaseException:
        message.continue_propagation()

    try:
        filters = get_filters(message.chat.id)
    except BaseException:
        message.continue_propagation()

    if not filters:
        message.continue_propagation()

    for trigger in filters:
        pro = fullmatch(trigger.keyword, name, flags=IGNORECASE)
        if pro:
            if trigger.f_mesg_id:
                msg_o = get_messages(LOG_ID, msg_ids=int(trigger.f_mesg_id))
                if msg_o and len(msg_o) > 0 and not msg_o[-1].empty:
                    msg = msg_o[-1]
                    reply_msg(message, msg)
                else:
                    edit(message, f'`{get_translation("filterResult")}`')
            elif trigger.reply:
                reply(message, trigger.reply)
            else:
                edit(message, f'`{get_translation("wrongFilter")}`')

    message.continue_propagation()


@sedenify(pattern='^.addfilter')
def add_filter(message):
    try:
        from sedenecem.sql.filters_sql import add_filter
    except BaseException:
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
                    edit(message, f'`{get_translation("filterError")}`')
                    return
                msg_id = msg_o.message_id
                send_log(get_translation('filterLog', ['`', message.chat.id, keyword]))
        else:
            edit(message, f'`{get_translation("wrongCommand")}`')

    if add_filter(str(message.chat.id), keyword, string, msg_id):
        edit(message, get_translation('filterAdded', ['**', '`', keyword]))
    else:
        edit(message, get_translation('filterUpdated', ['**', '`', keyword]))


@sedenify(pattern='^.stop')
def stop_filter(message):
    try:
        from sedenecem.sql.filters_sql import remove_filter
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    filt = extract_args(message)
    if not remove_filter(message.chat.id, filt):
        edit(message, get_translation('filterNotFound', ['**', '`', filt]))
    else:
        edit(message, get_translation('filterRemoved', ['**', '`', filt]))


@sedenify(pattern='^.stopall$')
def stop_filter_all(message):
    try:
        from sedenecem.sql.filters_sql import get_filters, remove_filter
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    filters = get_filters(message.chat.id)
    for filt in filters:
        remove_filter(message.chat.id, filt.keyword)
    filtwords = [i.keyword for i in filters]
    edit(message, get_translation('filterRemoved', ['**', '`', ', '.join(filtwords)]))


@sedenify(pattern='^.filters$')
def filters(message):
    try:
        from sedenecem.sql.filters_sql import get_filters
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    transact = f'`{get_translation("noFilter")}`'
    filters = get_filters(message.chat.id)
    for filt in filters:
        if transact == f'`{get_translation("noFilter")}`':
            transact = f'{get_translation("filterChats")}\n'
            transact += '`{}`\n'.format(filt.keyword)
        else:
            transact += '`{}`\n'.format(filt.keyword)

    edit(message, transact)


HELP.update({'filter': get_translation('filterInfo')})
