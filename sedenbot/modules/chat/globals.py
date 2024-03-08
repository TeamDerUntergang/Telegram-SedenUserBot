# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep

from pyrogram import enums
from pyrogram.types import ChatPermissions
from sedenbot import BRAIN, HELP, LOGS
from sedenbot.modules.chat.ban import get_reason
from sedenecem.core import (
    edit,
    extract_args_split,
    extract_user,
    get_translation,
    sedenify,
    send_log,
)


def globals_init():
    try:
        global sql, sql2
        from importlib import import_module

        sql = import_module('sedenecem.sql.gban_sql')
        sql2 = import_module('sedenecem.sql.gmute_sql')
    except Exception as e:
        sql = None
        sql2 = None
        LOGS.warn(get_translation('globalsSqlLog'))
        raise e


globals_init()


@sedenify(pattern='^.gban')
def gban_user(message):
    reply = message.reply_to_message
    edit(message, f'`{get_translation("banProcess")}`')

    find_user = extract_user(message)
    if len(find_user) < 1:
        return edit(message, f'`{get_translation("banFailUser")}`')

    reason = get_reason(message)

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotBanMyself")}`')
    except BaseException:
        pass

    for user in find_user:
        if user.id in BRAIN:
            return edit(
                message,
                get_translation('brainError', ['`', '**', user.first_name, user.id]),
            )
        try:
            if sql.is_gbanned(user.id):
                return edit(message, f'`{get_translation("alreadyBanned")}`')
            sql.gban(user.id)
            edit(
                message,
                get_translation(
                    'gbanResult',
                    ['**', user.first_name, user.id, '`', reason if reason else ''],
                ),
            )
            try:
                common_chats = message._client.get_common_chats(user.id)
                for i in common_chats:
                    i.ban_member(user.id)
            except BaseException:
                pass
            sleep(1)
            send_log(
                get_translation(
                    'gbanLog', [user.first_name, user.id, '`', reason if reason else '']
                )
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.(ung|gun)ban')
def ungban_user(message):
    args = extract_args_split(message)
    if len(args) > 1:
        return edit(message, f'`{get_translation("wrongCommand")}`')
    reply = message.reply_to_message
    edit(message, f'`{get_translation("unbanProcess")}`')

    find_user = extract_user(message)
    if len(find_user) < 1:
        return edit(message, f'`{get_translation("banFailUser")}`')

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotUnbanMyself")}`')
    except BaseException:
        pass

    for user in find_user:
        try:
            if not sql.is_gbanned(user.id):
                return edit(message, f'`{get_translation("alreadyUnbanned")}`')
            sql.ungban(user.id)

            def find_me(dialog):
                try:
                    return (
                        dialog.chat.get_member(me_id).privileges
                        and dialog.chat.get_member(
                            me_id
                        ).privileges.can_restrict_members
                    )
                except BaseException:
                    return False

            def find_member(dialog):
                try:
                    return (
                        dialog.chat.get_member(user.id)
                        and dialog.chat.get_member(user.id).restricted_by
                        and dialog.chat.get_member(user.id).restricted_by.id == me_id
                    )
                except BaseException:
                    return False

            try:
                dialogs = message._client.get_dialogs()
                me_id = message._client.me.id
                chats = [
                    dialog.chat
                    for dialog in dialogs
                    if (
                        dialog.chat.type
                        in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]
                        and find_me(dialog)
                        and find_member(dialog)
                    )
                ]
                for chat in chats:
                    chat.unban_member(user.id)
            except BaseException:
                pass
            edit(
                message,
                get_translation('unbanResult', ['**', user.first_name, user.id, '`']),
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.listgban$')
def gbanlist(message):
    users = sql.gbanned_users()
    if not users:
        return edit(message, f'`{get_translation("listEmpty")}`')
    gban_list = f'**{get_translation("gbannedUsers")}**\n'
    count = 0
    for i in users:
        count += 1
        gban_list += f'**{count} -** `{i.sender}`\n'
    return edit(message, gban_list)


@sedenify(incoming=True, outgoing=False)
def gban_check(message):
    user = message.from_user
    if sql.is_gbanned(user.id):
        try:
            chat = message.chat
            chat.ban_member(user.id)
        except BaseException:
            pass

    message.continue_propagation()


@sedenify(pattern='^.gmute')
def gmute_user(message):
    reply = message.reply_to_message
    edit(message, f'`{get_translation("muteProcess")}`')

    find_user = extract_user(message)
    if len(find_user) < 1:
        return edit(message, f'`{get_translation("banFailUser")}`')

    reason = get_reason(message)

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotMuteMyself")}`')
    except BaseException:
        pass

    for user in find_user:
        if user.id in BRAIN:
            return edit(
                message,
                get_translation('brainError', ['`', '**', user.first_name, user.id]),
            )
        try:
            if sql2.is_gmuted(user.id):
                return edit(message, f'`{get_translation("alreadyMuted")}`')
            sql2.gmute(user.id)
            edit(
                message,
                get_translation(
                    'gmuteResult',
                    ['**', user.first_name, user.id, '`', reason if reason else ''],
                ),
            )
            try:
                common_chats = message._client.get_common_chats(user.id)
                for i in common_chats:
                    i.restrict_member(user.id, permissions=ChatPermissions())
            except BaseException:
                pass
            sleep(1)
            send_log(
                get_translation(
                    'gmuteLog',
                    [user.first_name, user.id, '`', reason if reason else ''],
                )
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.(ung|gun)mute')
def ungmute_user(message):
    args = extract_args_split(message)
    if len(args) > 1:
        return edit(message, f'`{get_translation("wrongCommand")}`')
    reply = message.reply_to_message
    edit(message, f'`{get_translation("unmuteProcess")}`')

    find_user = extract_user(message)
    if len(find_user) < 1:
        return edit(message, f'`{get_translation("banFailUser")}`')

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotUnmuteMyself")}`')
    except BaseException:
        pass

    for user in find_user:
        try:
            if not sql2.is_gmuted(user.id):
                return edit(message, f'`{get_translation("alreadyUnmuted")}`')
            sql2.ungmute(user.id)
            try:
                common_chats = message._client.get_common_chats(user.id)
                for i in common_chats:
                    i.unban_member(user.id)
            except BaseException:
                pass
            edit(
                message,
                get_translation('unmuteResult', ['**', user.first_name, user.id, '`']),
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.listgmute$')
def gmutelist(message):
    users = sql2.gmuted_users()
    if not users:
        return edit(message, f'`{get_translation("listEmpty")}`')
    gmute_list = f'**{get_translation("gmutedUsers")}**\n'
    count = 0
    for i in users:
        count += 1
        gmute_list += f'**{count} -** `{i.sender}`\n'
    return edit(message, gmute_list)


@sedenify(incoming=True, outgoing=False)
def gmute_check(message):
    user = message.from_user
    if sql2.is_gmuted(user.id):
        sleep(0.1)
        message.delete()

        try:
            chat = message.chat
            chat.restrict_member(user.id, permissions=ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()


HELP.update({'globals': get_translation('globalsInfo')})
