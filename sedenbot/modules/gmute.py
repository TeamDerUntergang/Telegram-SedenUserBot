# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep

try:
    from pyrogram import ChatPermissions
except:
    from pyrogram.types import ChatPermissions

from sedenbot import BRAIN
from sedenecem.sql import gmute_sql as sql
from sedenecem.core import (edit, sedenify, send_log,
                            extract_args, get_translation)


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
        user_id = user.id
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
            message, get_translation(
                'brainError', [
                    '`', '**', user.first_name, user.id]))

    try:
        if sql.is_gmuted(user.id):
            return edit(message, f'`{get_translation("alreadyMuted")}`')
        sql.gmute(user.id)
        edit(
            message, get_translation(
                'gmuteResult', [
                    '**', user.first_name, user.id, '`']))
        sleep(1)
        send_log(get_translation('gmuteLog', ['**', user.first_name, user.id]))
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
        user_id = user.id
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
        if not sql.is_gmuted(user.id):
            return edit(message, f'`{get_translation("alreadyUnmuted")}`')
        sql.ungmute(user.id)
        edit(
            message, get_translation(
                'unmuteResult', [
                    '**', user.first_name, user.id, '`']))
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(incoming=True, outgoing=False, compat=False)
def gmute_check(client, message):
    gmuted = sql.is_gmuted(message.from_user.id)

    if gmuted:
        sleep(0.1)
        message.delete()

        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()
