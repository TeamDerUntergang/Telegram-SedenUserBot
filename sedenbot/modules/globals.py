# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep

from pyrogram.types import ChatPermissions
from sedenbot import BRAIN, HELP, LOGS, TEMP_SETTINGS
from sedenecem.core import edit, extract_args, get_translation, sedenify, send_log


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


@sedenify(pattern='^.gban', compat=False)
def gban_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("banProcess")}`')
    if args:
        try:
            user = client.get_users(args)
        except Exception:
            edit(message, f'`{get_translation("banFailUser")}`')
            return
    elif reply:
        user_id = reply.from_user.id
        user = client.get_users(user_id)
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotBanMyself")}`')
    except BaseException:
        pass

    if user.id in BRAIN:
        return edit(
            message,
            get_translation(
                'brainError', ['`', '**', user.first_name, user.id]),
        )

    try:
        if sql.is_gbanned(user.id):
            return edit(message, f'`{get_translation("alreadyBanned")}`')
        sql.gban(user.id)
        edit(
            message,
            get_translation(
                'gbanResult', ['**', user.first_name, user.id, '`']),
        )
        try:
            common_chats = client.get_common_chats(user.id)
            for i in common_chats:
                i.ban_member(user.id)
        except BaseException:
            pass
        sleep(1)
        send_log(get_translation('gbanLog', [user.first_name, user.id, '`']))
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.(ung|gun)ban', compat=False)
def ungban_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("unbanProcess")}`')
    if args:
        try:
            user = client.get_users(args)
        except Exception:
            edit(message, f'`{get_translation("banFailUser")}`')
            return
    elif reply:
        user_id = reply.from_user.id
        user = client.get_users(user_id)
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotUnbanMyself")}`')
    except BaseException:
        pass

    try:
        if not sql.is_gbanned(user.id):
            return edit(message, f'`{get_translation("alreadyUnbanned")}`')
        sql.ungban(user.id)

        def find_me(dialog):
            try:
                return dialog.chat.get_member(me_id).can_restrict_members
            except BaseException:
                return False

        def find_member(dialog):
            try:
                return (dialog.chat.get_member(user.id)
                    and dialog.chat.get_member(user.id).restricted_by
                    and dialog.chat.get_member(user.id).restricted_by.id == me_id)
            except BaseException:
                return False

        try:
            dialogs = client.iter_dialogs()
            me_id = TEMP_SETTINGS['ME'].id
            chats = [
                dialog.chat
                for dialog in dialogs
                if (
                    'group' in dialog.chat.type
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
            get_translation(
                'unbanResult', ['**', user.first_name, user.id, '`']),
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


@sedenify(incoming=True, outgoing=False, compat=False)
def gban_check(client, message):
    if sql.is_gbanned(message.from_user.id):
        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            client.ban_chat_member(chat_id, user_id)
        except BaseException:
            pass

    message.continue_propagation()


@sedenify(pattern='^.gmute', compat=False)
def gmute_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("muteProcess")}`')
    if len(args):
        try:
            user = client.get_users(args)
        except Exception:
            edit(message, f'`{get_translation("banFailUser")}`')
            return
    elif reply:
        user_id = reply.from_user.id
        user = client.get_users(user_id)
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotMuteMyself")}`')
    except BaseException:
        pass

    if user.id in BRAIN:
        return edit(
            message,
            get_translation(
                'brainError', ['`', '**', user.first_name, user.id]),
        )

    try:
        if sql2.is_gmuted(user.id):
            return edit(message, f'`{get_translation("alreadyMuted")}`')
        sql2.gmute(user.id)
        edit(
            message,
            get_translation(
                'gmuteResult', ['**', user.first_name, user.id, '`']),
        )
        try:
            common_chats = client.get_common_chats(user.id)
            for i in common_chats:
                i.restrict_member(user.id, ChatPermissions())
        except BaseException:
            pass
        sleep(1)
        send_log(get_translation('gmuteLog', [user.first_name, user.id, '`']))
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.ungmute', compat=False)
def ungmute_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("unmuteProcess")}`')
    if len(args):
        try:
            user = client.get_users(args)
        except Exception:
            edit(message, f'`{get_translation("banFailUser")}`')
            return
    elif reply:
        user_id = reply.from_user.id
        user = client.get_users(user_id)
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotUnmuteMyself")}`')
    except BaseException:
        pass

    try:
        if not sql2.is_gmuted(user.id):
            return edit(message, f'`{get_translation("alreadyUnmuted")}`')
        sql2.ungmute(user.id)
        try:
            common_chats = client.get_common_chats(user.id)
            for i in common_chats:
                i.unban_member(user.id)
        except BaseException:
            pass
        edit(
            message,
            get_translation('unmuteResult', [
                            '**', user.first_name, user.id, '`']),
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


@sedenify(incoming=True, outgoing=False, compat=False)
def gmute_check(client, message):
    if sql2.is_gmuted(message.from_user.id):
        sleep(0.1)
        message.delete()

        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()


HELP.update({'globals': get_translation('globalsInfo')})
