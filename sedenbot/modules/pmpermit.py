# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from re import VERBOSE
from sedenbot import (
    HELP,
    LOGS,
    PM_AUTO_BAN,
    PM_MSG_COUNT,
    PM_UNAPPROVED,
    TEMP_SETTINGS,
)
from sedenbot.modules.chat import is_muted
from sedenecem.core import edit, get_translation, reply, sedenify, send_log
from sqlalchemy.exc import IntegrityError

# ========================= CONSTANTS ============================
UNAPPROVED_MSG = PM_UNAPPROVED or get_translation('pmpermitMessage', ['`'])
# =================================================================


def pmpermit_init():
    try:
        global sql
        from importlib import import_module

        sql = import_module('sedenecem.sql.pm_permit_sql')
    except Exception as e:
        sql = None
        LOGS.warn(get_translation('pmpermitSqlLog'))
        raise e


pmpermit_init()


@sedenify(
    incoming=True,
    outgoing=True,
    disable_edited=True,
    disable_notify=True,
    group=False,
    compat=False,
    bot=False,
)
def permitpm(client, message):
    if not PM_AUTO_BAN:
        message.continue_propagation()
    else:
        if auto_accept(client, message) or message.from_user.is_self:
            message.continue_propagation()

        if message.chat.id != 777000:
            try:
                from sedenecem.sql.pm_permit_sql import is_approved
            except BaseException:
                pass

            apprv = is_approved(message.chat.id)
            notifsoff = is_muted(-1)

            if not apprv and message.text != UNAPPROVED_MSG:
                if message.chat.id in TEMP_SETTINGS['PM_LAST_MSG']:
                    prevmsg = TEMP_SETTINGS['PM_LAST_MSG'][message.chat.id]
                    if message.text != prevmsg:
                        for message in _find_unapproved_msg(client, message.chat.id):
                            message.delete()
                        if TEMP_SETTINGS['PM_COUNT'][message.chat.id] < (PM_MSG_COUNT - 1):
                            ret = reply(message, UNAPPROVED_MSG)
                            TEMP_SETTINGS['PM_LAST_MSG'][message.chat.id] = ret.text
                else:
                    ret = reply(message, UNAPPROVED_MSG)
                    if ret.text:
                        TEMP_SETTINGS['PM_LAST_MSG'][message.chat.id] = ret.text

                if notifsoff:
                    client.read_history(message.chat.id)

                if message.chat.id not in TEMP_SETTINGS['PM_COUNT']:
                    TEMP_SETTINGS['PM_COUNT'][message.chat.id] = 1
                else:
                    TEMP_SETTINGS['PM_COUNT'][message.chat.id] = TEMP_SETTINGS['PM_COUNT'][message.chat.id] + 1

                if TEMP_SETTINGS['PM_COUNT'][message.chat.id] > (PM_MSG_COUNT - 1):
                    reply(message, f'`{get_translation("pmpermitBlock")}`')

                    try:
                        del TEMP_SETTINGS['PM_COUNT'][message.chat.id]
                        del TEMP_SETTINGS['PM_LAST_MSG'][message.chat.id]
                    except BaseException:
                        pass

                    client.block_user(message.chat.id)

                    send_log(
                        get_translation(
                            'pmpermitLog', [message.chat.first_name, message.chat.id]
                        )
                    )

    message.continue_propagation()


def auto_accept(client, message):
    self_user = TEMP_SETTINGS['ME']
    if message.chat.id not in [self_user.id, 777000]:
        try:
            from sedenecem.sql.pm_permit_sql import approve, is_approved
        except BaseException:
            return False

        chat = message.chat
        if is_approved(chat.id):
            return True

        for msg in client.get_history(chat.id, limit=1, reverse=True):
            # chat.id in TEMP_SETTINGS['PM_LAST_MSG']
            #    and msg.text != UNAPPROVED_MSG
            #    and

            if (
                 msg.from_user.id == self_user.id
            ):
                try:
                    del TEMP_SETTINGS['PM_COUNT'][chat.id]
                    del TEMP_SETTINGS['PM_LAST_MSG'][chat.id]
                except BaseException:
                    pass

                try:
                    approve(chat.id)
                    for message in _find_unapproved_msg(client, chat.id):
                        message.delete()
                    send_log(
                        get_translation('pmAutoAccept', [chat.first_name, chat.id])
                    )
                    return True
                except BaseException:
                    pass

    return False


@sedenify(outgoing=True, pattern='^.notifoff$')
def notifoff(message):
    try:
        from sedenecem.sql.keep_read_sql import kread
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    kread(str(-1))
    edit(message, f'`{get_translation("pmNotifOff")}`')


@sedenify(outgoing=True, pattern='^.notifon$')
def notifon(message):
    try:
        from sedenecem.sql.keep_read_sql import unkread
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    unkread(str(-1))
    edit(message, f'`{get_translation("pmNotifOn")}`')


@sedenify(outgoing=True, pattern='^.approve$', compat=False)
def approvepm(client, message):
    try:
        from sedenecem.sql.pm_permit_sql import approve
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            edit(message, f'`{get_translation("cannotApproveMyself")}`')
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == 'private':
            edit(message, f'`{get_translation("pmApproveError")}`')
            return
        name0 = aname.first_name
        uid = aname.id

    try:
        approve(uid)
        edit(message, get_translation('pmApproveSuccess', [name0, uid, '`']))
        send_log(get_translation('pmApproveLog', [name0, uid]))
        for message in _find_unapproved_msg(client, message.chat.id):
            message.delete()
    except IntegrityError:
        edit(message, f'`{get_translation("pmApproveError2")}`')
        return


@sedenify(outgoing=True, pattern="^.disapprove$")
def disapprovepm(message):
    try:
        from sedenecem.sql.pm_permit_sql import dissprove
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            edit(message, f'`{get_translation("cannotDisapproveMyself")}`')
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == 'private':
            edit(message, f'`{get_translation("pmApproveError")}`')
            return
        name0 = aname.first_name
        uid = aname.id

    dissprove(uid)

    edit(message, get_translation('pmDisapprove', [name0, uid, '`']))

    send_log(get_translation('pmDisapprove', [name0, uid, '`']))


def _find_unapproved_msg(client, chat_id):
    try:
        return client.search_messages(
            chat_id, from_user='me', limit=10, query=UNAPPROVED_MSG
        )
    except BaseException:
        return []


HELP.update({'pmpermit': get_translation('pmpermitInfo')})
