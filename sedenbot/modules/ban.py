# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove
from time import sleep

from PIL import Image
from pyrogram import enums
from pyrogram.errors import (
    ImageProcessFailed,
    MessageTooLong,
    PhotoCropSizeSmall,
    UserAdminInvalid,
)
from pyrogram.types import ChatPermissions, ChatPrivileges
from sedenbot import BRAIN, HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    extract_args_arr,
    extract_user,
    get_download_dir,
    get_translation,
    is_admin,
    reply_doc,
    sedenify,
    send_log,
)


def get_reason(message):
    args = extract_args(message)
    reply = message.reply_to_message
    if reply:
        if args:
            reason = get_translation('banReason', ['**', '`', args])
        else:
            reason = ''
    else:
        text = args.split(' ', 1)
        if len(text) > 1:
            reason = get_translation('banReason', ['**', '`', text[1]])
        else:
            reason = ''
    pass
    return reason


@sedenify(pattern='^.ban', private=False, admin=True)
def ban_user(message):
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
            chat = message.chat
            chat.ban_member(user.id)
            edit(
                message,
                get_translation(
                    'banResult',
                    ['**', user.first_name, user.id, '`', reason if reason else ''],
                ),
            )
            sleep(1)
            send_log(
                get_translation(
                    'banLog',
                    [
                        user.first_name,
                        user.id,
                        chat.title,
                        '`',
                        chat.id,
                        reason if reason else '',
                    ],
                )
            )
        except UserAdminInvalid:
            edit(message, f'`{get_translation("banAdminError")}`')
        except BaseException as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.unban', private=False, admin=True)
def unban_user(message):
    args = extract_args_arr(message)
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
            chat = message.chat
            chat.unban_member(user.id)
            edit(
                message,
                get_translation('unbanResult', ['**', user.first_name, user.id, '`']),
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.kick', private=False, admin=True)
def kick_user(message):
    reply = message.reply_to_message
    edit(message, f'`{get_translation("kickProcess")}`')

    find_user = extract_user(message)
    if len(find_user) < 1:
        return edit(message, f'`{get_translation("banFailUser")}`')

    reason = get_reason(message)

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotKickMyself")}`')
    except BaseException:
        pass

    for user in find_user:
        if user.id in BRAIN:
            return edit(
                message,
                get_translation('brainError', ['`', '**', user.first_name, user.id]),
            )
        try:
            chat = message.chat
            chat.ban_member(user.id)
            chat.unban_member(user.id)
            edit(
                message,
                get_translation(
                    'kickResult',
                    ['**', user.first_name, user.id, '`', reason if reason else ''],
                ),
            )
            sleep(1)
            send_log(
                get_translation(
                    'kickLog',
                    [
                        user.first_name,
                        user.id,
                        chat.title,
                        '`',
                        chat.id,
                        reason if reason else '',
                    ],
                )
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.mute', private=False, admin=True)
def mute_user(message):
    try:
        from sedenecem.sql import mute_sql as sql
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

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
            chat = message.chat
            if sql.is_muted(chat.id, user.id):
                return edit(message, 'kullanici zaten susturulmus')
            sql.mute(chat.id, user.id)
            edit(
                message,
                get_translation(
                    'muteResult',
                    ['**', user.first_name, user.id, '`', reason if reason else ''],
                ),
            )
            sleep(1)
            send_log(
                get_translation(
                    'muteLog',
                    [
                        user.first_name,
                        user.id,
                        chat.title,
                        '`',
                        chat.id,
                        reason if reason else '',
                    ],
                )
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.unmute', private=False, admin=True)
def unmute_user(message):
    try:
        from sedenecem.sql import mute_sql as sql
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    args = extract_args_arr(message)
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
            return edit(message, f'`{get_translation("cannotMuteMyself")}`')
    except BaseException:
        pass

    for user in find_user:
        try:
            chat = message.chat
            sql.unmute(chat.id, user.id)
            chat.unban_member(user.id)
            edit(
                message,
                get_translation('unmuteResult', ['**', user.first_name, user.id, '`']),
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.promote', admin=True, private=False, compat=False)
def promote_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    rank = None
    edit(message, f'`{get_translation("promoteProcess")}`')

    find_user = extract_user(message)
    if len(find_user) < 1:
        return edit(message, f'`{get_translation("banFailUser")}`')

    if reply:
        if args:
            rank = args
        else:
            rank = ''
    else:
        text = args.split(' ', 1)
        if len(text) > 1:
            rank = text[1]
        else:
            rank = ''

    for user in find_user:
        try:
            chat = message.chat
            chat.promote_member(
                user.id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                ),
            )
            if rank is not None:
                if len(rank) > 16:
                    rank = rank[:16]
                client.set_administrator_title(chat.id, user.id, rank)
            edit(
                message,
                get_translation('promoteResult', ['**', user.first_name, user.id, '`']),
            )
            sleep(1)
            send_log(
                get_translation(
                    'promoteLog',
                    [user.first_name, user.id, chat.title, '`', chat.id],
                )
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.demote', private=False, admin=True)
def demote_user(message):
    args = extract_args_arr(message)
    if len(args) > 1:
        return edit(message, f'`{get_translation("wrongCommand")}`')
    reply = message.reply_to_message
    edit(message, f'`{get_translation("demoteProcess")}`')

    find_user = extract_user(message)
    if len(find_user) < 1:
        return edit(message, f'`{get_translation("banFailUser")}`')

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotDemoteMyself")}`')
    except BaseException:
        pass

    for user in find_user:
        try:
            chat = message.chat
            chat.promote_member(
                user.id,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ),
            )
            edit(
                message,
                get_translation('demoteResult', ['**', user.first_name, user.id, '`']),
            )
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return


@sedenify(pattern='^.pin', private=False, admin=True)
def pin_message(message):
    args = extract_args(message).lower()
    reply = message.reply_to_message

    if reply:
        try:
            chat = message.chat
            if args == 'loud':
                reply.pin(disable_notification=False)
            else:
                reply.pin(disable_notification=True)
            edit(message, f'`{get_translation("pinResult")}`')
            sleep(1)
            send_log(get_translation('pinLog', [message.chat.title, '`', chat.id]))
        except Exception as e:
            return edit(message, get_translation('banError', ['`', '**', e]))
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')


@sedenify(pattern='^.unpin', private=False, admin=True)
def unpin_message(message):
    args = extract_args(message).lower()
    reply = message.reply_to_message
    chat = message.chat
    if reply:
        try:
            reply.unpin()
            message.delete()
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return
    elif 'all' in args:
        try:
            chat.unpin_all_messages()
            message.delete()
        except Exception as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')


@sedenify(pattern='^.(admins|bots|user(s|sdel))$', compat=False, private=False)
def get_users(client, message):
    args = message.text.split(' ', 1)
    users = args[0][1:5] == 'user'
    showdel = users and args[0][-3:] == 'del'
    bots = not users and args[0][1:5] == 'bots'
    admins = not bots and args[0][1:7] == 'admins'

    out = ''
    if users:
        out = get_translation(
            'userlist',
            [
                '**',
                f'{get_translation("deleted") if showdel else ""}',
                '`',
                message.chat.title,
            ],
        )
        filtr = enums.ChatMembersFilter.SEARCH
    elif admins:
        out = get_translation('adminlist', ['**', '`', message.chat.title])
        filtr = enums.ChatMembersFilter.ADMINISTRATORS
    elif bots:
        out = get_translation('botlist', ['**', '`', message.chat.title])
        filtr = enums.ChatMembersFilter.BOTS

    try:
        chat_id = message.chat.id
        find = client.get_chat_members(chat_id, filter=filtr)
        for i in find:
            if not i.user.is_deleted and showdel:
                continue
            name = f'[{get_translation("deletedAcc") if i.user.is_deleted else i.user.first_name}](tg://user?id={i.user.id}) | `{i.user.id}`'
            out += f'\n`•`  **{name}**'
    except Exception as e:
        out += f'\n{get_translation("banError", ["`", "**", e])}'

    try:
        edit(message, out)
    except MessageTooLong:
        edit(message, f'`{get_translation("outputTooLarge")}`')
        file = open('userslist.txt', 'w+')
        file.write(out)
        file.close()
        reply_doc(
            message,
            'userslist.txt',
            caption=get_translation(
                'userlist',
                [
                    '**',
                    f'{get_translation("deleted") if showdel else ""}',
                    '`',
                    message.chat.title,
                ],
            ),
            delete_after_send=True,
            delete_orig=True,
        )


@sedenify(pattern='^.zombies', private=False, compat=False)
def zombie_accounts(client, message):
    args = extract_args(message).lower()
    chat = message.chat
    count = 0
    msg = f'`{get_translation("zombiesNoAccount")}`'

    if args != 'clean':
        edit(message, f'`{get_translation("zombiesFind")}`')
        for i in client.get_chat_members(chat.id):
            if i.user.is_deleted:
                count += 1
                sleep(1)
        if count > 0:
            msg = get_translation('zombiesFound', ['**', '`', count])
        return edit(message, msg)

    if not is_admin(message):
        edit(message, f'`{get_translation("adminUsage")}`')
        return message.continue_propagation()

    edit(message, f'`{get_translation("zombiesRemove")}`')
    count = 0
    users = 0

    for i in client.get_chat_members(chat.id):
        if i.user.is_deleted:
            try:
                chat.ban_member(i.user.id)
            except UserAdminInvalid:
                count -= 1
                users += 1
            except BaseException:
                return edit(message, f'`{get_translation("zombiesError")}`')
            chat.unban_member(i.user.id)
            count += 1

    if count > 0:
        msg = get_translation('zombiesResult', ['**', '`', count])

    if users > 0:
        msg = get_translation('zombiesResult2', ['**', '`', count, users])

    edit(message, msg)
    sleep(2)
    message.delete()

    send_log(get_translation('zombiesLog', ['**', '`', count, chat.title, chat.id]))


@sedenify(pattern='^.setgpic$', admin=True, private=False)
def set_group_photo(message):
    reply = message.reply_to_message
    photo = None
    if (
        reply
        and reply.media
        and (
            reply.photo
            or (reply.sticker and not reply.sticker.is_animated)
            or (reply.document and 'image' in reply.document.mime_type)
        )
    ):
        photo = download_media_wc(reply, 'group_photo.jpg')
    else:
        edit(message, f'{get_translation("mediaInvalid")}`')
        return

    if photo:
        image = Image.open(photo)
        width, height = image.size
        maxSize = (640, 640)
        ratio = min(maxSize[0] / width, maxSize[1] / height)
        image = image.resize((int(width * ratio), int(height * ratio)))
        new_photo = f'{get_download_dir()}/group_photo_new.png'
        image.save(new_photo)
        try:
            chat = message.chat
            chat.set_photo(photo=new_photo)
            remove(photo)
            remove(new_photo)
            edit(message, f'`{get_translation("groupPicChanged")}`')
        except PhotoCropSizeSmall:
            edit(message, f'`{get_translation("ppSmall")}`')
        except ImageProcessFailed:
            edit(message, f'`{get_translation("ppError")}`')
        except BaseException as e:
            edit(message, get_translation('banError', ['`', '**', e]))
            return
    else:
        edit(message, f'`{get_translation("ppError")}`')


@sedenify(incoming=True, outgoing=False)
def mute_check(message):
    try:
        from sedenecem.sql import mute_sql as sql
    except BaseException:
        return

    chat = message.chat
    user = message.from_user
    muted = sql.is_muted(chat.id, user.id)

    if muted:
        sleep(0.1)
        message.delete()

        try:
            chat.restrict_member(user.id, permissions=ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()


HELP.update({'admin': get_translation('adminInfo')})
