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
from pyrogram.errors import (
    ImageProcessFailed,
    MessageTooLong,
    PhotoCropSizeSmall,
    UserAdminInvalid,
)
from pyrogram.types import ChatPermissions
from sedenbot import BRAIN, HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_download_dir,
    get_translation,
    is_admin,
    reply_doc,
    sedenify,
    send_log,
)


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
            get_translation('brainError', ['`', '**', user.first_name, user.id]),
        )

    try:
        chat_id = message.chat.id
        client.ban_chat_member(chat_id, user.id)
        edit(
            message, get_translation('banResult', ['**', user.first_name, user.id, '`'])
        )
        sleep(1)
        send_log(
            get_translation(
                'banLog',
                [user.first_name, user.id, message.chat.title, '`', chat_id],
            )
        )
    except UserAdminInvalid:
        edit(message, f'`{get_translation("banAdminError")}`')
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
        chat_id = message.chat.id
        client.unban_chat_member(chat_id, user.id)
        edit(
            message,
            get_translation('unbanResult', ['**', user.first_name, user.id, '`']),
        )
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
            message,
            get_translation('brainError', ['`', '**', user.first_name, user.id]),
        )

    try:
        chat_id = message.chat.id
        client.ban_chat_member(chat_id, user.id)
        client.unban_chat_member(chat_id, user.id)
        edit(
            message,
            get_translation('kickResult', ['**', user.first_name, user.id, '`']),
        )
        sleep(1)
        send_log(
            get_translation(
                'kickLog',
                [
                    user.first_name,
                    user.id,
                    message.chat.title,
                    '`',
                    message.chat.id,
                ],
            )
        )
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.mute', compat=False, private=False, admin=True)
def mute_user(client, message):
    try:
        from sedenecem.sql import mute_sql as sql
    except BaseException:
        edit(message,f'`{get_translation("nonSqlMode")}`')
        return

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
            get_translation('brainError', ['`', '**', user.first_name, user.id]),
        )

    try:
        chat_id = message.chat.id
        if sql.is_muted(chat_id, user.id):
            return
        sql.mute(chat_id, user.id)
        edit(
            message,
            get_translation('muteResult', ['**', user.first_name, user.id, '`']),
        )
        sleep(1)
        send_log(
            get_translation(
                'muteLog',
                [user.first_name, user.id, message.chat.title, '`', chat_id],
            )
        )
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.unmute', compat=False, private=False, admin=True)
def unmute_user(client, message):
    try:
        from sedenecem.sql import mute_sql as sql
    except BaseException:
        edit(message,f'`{get_translation("nonSqlMode")}`')
        return

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
        chat_id = message.chat.id
        sql.unmute(chat_id, user.id)
        client.unban_chat_member(chat_id, user.id)
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
    if reply:
        try:
            user_id = reply.from_user.id
            user = client.get_users(user_id)
            rank = args
        except Exception:
            return edit(message, f'`{get_translation("banFailUser")}`')
    elif ' ' not in args:
        try:
            user = client.get_users(args)
        except Exception:
            return edit(message, f'`{get_translation("banFailUser")}`')
    elif args:
        try:
            arr = args.split(' ', 1)
            user = client.get_users(arr[0])
            rank = arr[1]
        except Exception:
            return edit(message, f'`{get_translation("banFailUser")}`')
    else:
        return edit(message, f'`{get_translation("banFailUser")}`')

    try:
        chat_id = message.chat.id
        client.promote_chat_member(
            chat_id,
            user.id,
            can_change_info=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=True,
        )
        if rank is not None:
            if len(rank) > 16:
                rank = rank[:16]
            client.set_administrator_title(chat_id, user.id, rank)
        edit(
            message,
            get_translation('promoteResult', ['**', user.first_name, user.id, '`']),
        )
        sleep(1)
        send_log(
            get_translation(
                'promoteLog',
                [user.first_name, user.id, message.chat.title, '`', chat_id],
            )
        )
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
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotDemoteMyself")}`')
    except BaseException:
        pass

    try:
        chat_id = message.chat.id
        client.promote_chat_member(
            chat_id,
            user.id,
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        )
        edit(
            message,
            get_translation('demoteResult', ['**', user.first_name, user.id, '`']),
        )
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
        message_id = reply.message_id
        client.pin_chat_message(chat_id, message_id)
        edit(message, f'`{get_translation("pinResult")}`')
        sleep(1)
        send_log(get_translation('pinLog', [message.chat.title, '`', chat_id]))
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.unpin', compat=False, private=False, admin=True)
def unpin_message(client, message):
    args = extract_args(message)
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
            client.unpin_all_chat_messages(chat.id)
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
        filtr = 'all'
    elif admins:
        out = get_translation('adminlist', ['**', '`', message.chat.title])
        filtr = 'administrators'
    elif bots:
        out = get_translation('botlist', ['**', '`', message.chat.title])
        filtr = 'bots'

    try:
        chat_id = message.chat.id
        find = client.iter_chat_members(chat_id, filter=filtr)
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
    chat_id = message.chat.id
    count = 0
    msg = f'`{get_translation("zombiesNoAccount")}`'

    if args != 'clean':
        edit(message, f'`{get_translation("zombiesFind")}`')
        for i in client.iter_chat_members(chat_id):
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

    for i in client.iter_chat_members(chat_id):
        if i.user.is_deleted:
            try:
                client.ban_chat_member(chat_id, i.user.id)
            except UserAdminInvalid:
                count -= 1
                users += 1
            except BaseException:
                return edit(message, f'`{get_translation("zombiesError")}`')
            client.unban_chat_member(chat_id, i.user.id)
            count += 1

    if count > 0:
        msg = get_translation('zombiesResult', ['**', '`', count])

    if users > 0:
        msg = get_translation('zombiesResult2', ['**', '`', count, users])

    edit(message, msg)
    sleep(2)
    message.delete()

    send_log(
        get_translation('zombiesLog', ['**', '`', count, message.chat.title, chat_id])
    )


@sedenify(pattern='^.setgpic$', compat=False, admin=True, private=False)
def set_group_photo(client, message):
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
            client.set_chat_photo(chat_id=message.chat.id, photo=new_photo)
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


@sedenify(incoming=True, outgoing=False, compat=False)
def mute_check(client, message):
    try:
        from sedenecem.sql import mute_sql as sql
    except BaseException:
        return

    muted = sql.is_muted(message.chat.id, message.from_user.id)

    if muted:
        sleep(0.1)
        message.delete()

        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()


HELP.update({'admin': get_translation('adminInfo')})
