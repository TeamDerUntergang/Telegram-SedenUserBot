# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep
from pyrogram import ChatPermissions

from sedenbot import KOMUT, BRAIN
from sedenecem.core import (edit, sedenify, send_log,
                            extract_args, get_translation)


@sedenify(pattern='^.ban', compat=False, private=False, admin=True)
def ban_user(client, message):
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
        user_id = user.id
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
            message, get_translation(
                'brainError', [
                    '`', '**', user.first_name, user.id]))

    if user is not None:
        try:
            chat_id = message.chat.id
            client.kick_chat_member(chat_id, user.id)
            edit(
                message, get_translation(
                    'banResult', [
                        '**', user.first_name, user.id, '`']))
            sleep(1)
            send_log(
                get_translation(
                    'banLog',
                    ['**', user.first_name, user.id, message.chat.title,
                     '`', message.chat.id]))
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.unban', compat=False, private=False, admin=True)
def unban_user(client, message):
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
        user_id = user.id
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotUnbanMyself")}`')
    except BaseException:
        pass

    if user is not None:
        try:
            chat_id = message.chat.id
            client.unban_chat_member(chat_id, user.id)
            edit(
                message, get_translation(
                    'unbanResult', [
                        '**', user.first_name, user.id, '`']))
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.kick', compat=False, private=False, admin=True)
def kick_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("kickProcess")}`')
    if args:
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
            return edit(message, f'`{get_translation("cannotKickMyself")}`')
    except BaseException:
        pass

    if user.id in BRAIN:
        return edit(
            message, get_translation(
                'brainError', [
                    '`', '**', user.first_name, user.id]))

    if user is not None:
        try:
            chat_id = message.chat.id
            client.kick_chat_member(chat_id, user.id)
            client.unban_chat_member(chat_id, user.id)
            edit(
                message, get_translation(
                    'kickResult', [
                        '**', user.first_name, user.id, '`']))
            sleep(1)
            send_log(
                get_translation(
                    'kickLog', [
                        '**', user.first_name, user.id, message.chat.title, '`', message.chat.id]))
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.mute', compat=False, private=False, admin=True)
def mute_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("muteProcess")}`')
    if args:
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

    if user is not None:
        try:
            chat_id = message.chat.id
            client.restrict_chat_member(chat_id, user.id, ChatPermissions())
            edit(
                message, get_translation(
                    'muteResult', [
                        '**', user.first_name, user.id, '`']))
            sleep(1)
            send_log(
                get_translation(
                    'muteLog', [
                        '**', user.first_name, user.id, message.chat.title, '`', message.chat.id]))
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.unmute', compat=False, private=False, admin=True)
def unmute_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("unmuteProcess")}`')
    if args:
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
            return edit(message, f'`{get_translation("cannotUnbanMyself")}`')
    except BaseException:
        pass

    if user is not None:
        try:
            chat_id = message.chat.id
            client.unban_chat_member(chat_id, user.id)
            edit(
                message, get_translation(
                    'unmuteResult', [
                        '**', user.first_name, user.id, '`']))
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.promote', compat=False, private=False, admin=True)
def promote_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("promoteProcess")}`')
    if args:
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
    if user is not None:
        try:
            chat_id = message.chat.id
            client.promote_chat_member(chat_id, user.id,
                                       can_change_info=True,
                                       can_delete_messages=True,
                                       can_restrict_members=True,
                                       can_invite_users=True,
                                       can_pin_messages=True,
                                       can_promote_members=True)
            edit(
                message, get_translation(
                    'promoteResult', [
                        '**', user.first_name, user.id, '`']))
            sleep(1)
            send_log(
                get_translation(
                    'promoteLog', [
                        '**', user.first_name, user.id, message.chat.title, '`', message.chat.id]))
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.demote', compat=False, private=False, admin=True)
def demote_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("demoteProcess")}`')
    if args:
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
            return edit(message, f'`{get_translation("cannotDemoteMyself")}`')
    except BaseException:
        pass

    if user is not None:
        try:
            chat_id = message.chat.id
            client.promote_chat_member(chat_id, user.id,
                                       can_change_info=False,
                                       can_delete_messages=False,
                                       can_restrict_members=False,
                                       can_invite_users=False,
                                       can_pin_messages=False,
                                       can_promote_members=False)
            edit(
                message, get_translation(
                    'demoteResult', [
                        '**', user.first_name, user.id, '`']))
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.pin$', compat=False, private=False, admin=True)
def pin_message(client, message):
    reply = message.reply_to_message

    if not reply:
        return edit(message, f'`{get_translation("wrongCommand")}`')

    try:
        chat_id = message.chat.id
        message_id = message.reply_to_message.message_id
        client.pin_chat_message(chat_id, message_id)
        edit(message, f'`{get_translation("pinResult")}`')
        sleep(1)
        send_log(
            get_translation(
                'pinLog', [
                    '**', message.chat.title, '`', message.chat.id]))
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.unpin$', compat=False, private=False, admin=True)
def pin_message(client, message):
    reply = message.reply_to_message

    if not reply:
        return edit(message, f'`{get_translation("wrongCommand")}`')

    try:
        chat_id = message.chat.id
        message_id = message.reply_to_message.message_id
        client.unpin_chat_message(chat_id)
        message.delete()
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


KOMUT.update({'admin': get_translation('adminInfo')})
