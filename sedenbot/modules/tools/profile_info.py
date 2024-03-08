# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from pyrogram import enums
from pyrogram.errors import PeerIdInvalid
from pyrogram.raw.functions.messages import GetOnlines
from sedenbot import BLACKLIST, BRAIN, HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_user,
    extract_args,
    get_translation,
    reply_img,
    sedenify,
)


@sedenify(pattern='^.whois')
def who_is(message):
    find_user = extract_user(message)
    reply = message.reply_to_message
    media_perm = None
    edit(message, f'`{get_translation("whoisProcess")}`')

    if len(find_user) < 1:
        return edit(message, f'`{get_translation("banFailUser")}`')

    if message.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
        perm = message.chat.permissions
        media_perm = perm.can_send_media_messages

    if message.chat.type == enums.ChatType.PRIVATE:
        media_perm = True

    for reply_user in find_user:
        try:
            reply_chat = message._client.get_chat(reply_user.id)
        except Exception:
            return edit(message, f'`{get_translation("whoisError")}`')
        if reply_user or reply_chat is not None:
            try:
                user_photo = reply_user.photo.big_file_id
                photo = download_media_wc(user_photo, 'photo.png')
            except BaseException:
                photo = None
                pass

            first_name = reply_user.first_name or get_translation('notSet')
            last_name = reply_user.last_name or get_translation('notSet')
            username = (
                f'@{reply_user.username}'
                if reply_user.username
                else get_translation('notSet')
            )
            user_id = reply_user.id
            photos = message._client.get_chat_photos_count(user_id)
            dc_id = reply_user.dc_id or get_translation('notSet')
            bot = reply_user.is_bot
            chats = len(message._client.get_common_chats(user_id))
            premium = reply_user.is_premium
            bio = reply_chat.bio or get_translation('notSet')
            status = reply_user.status
            user_utils = UserUtils(BRAIN, BLACKLIST)
            last_seen = user_utils.last_seen(bot, status)
            sudo = user_utils.sudo_check(user_id)
            blacklist = user_utils.blacklist_check(user_id)

            caption = get_translation(
                'whoisResult',
                [
                    '**',
                    '`',
                    first_name,
                    last_name,
                    username,
                    user_id,
                    photos,
                    dc_id,
                    chats,
                    '✅' if premium else '❌',
                    bio,
                    last_seen,
                    sudo if sudo else '',
                    blacklist if blacklist else '',
                ],
            )

    if photo and media_perm:
        reply_img(reply or message, photo, caption=caption, delete_file=True)
        message.delete()
    else:
        return edit(message, caption)


class UserUtils:
    def __init__(self, brain, blacklist):
        self.brain = brain
        self.blacklist = blacklist

    def last_seen(self, bot, status):
        status_list = {
            enums.UserStatus.ONLINE: get_translation('statusOnline'),
            enums.UserStatus.OFFLINE: get_translation('statusOffline'),
            enums.UserStatus.RECENTLY: get_translation('statusRecently'),
            enums.UserStatus.LAST_WEEK: get_translation('statusWeek'),
            enums.UserStatus.LAST_MONTH: get_translation('statusMonth'),
            enums.UserStatus.LONG_AGO: get_translation('statusLong')
        }
        if bot:
            return 'BOT'
        elif status in status_list:
            return status_list[status]

    def sudo_check(self, user_id):
        if user_id in self.brain:
            return get_translation('sudoCheck')

    def blacklist_check(self, user_id):
        if user_id in self.blacklist:
            return get_translation('blacklistCheck')


@sedenify(pattern='^.ginfo')
def get_chat_info(message):
    args = extract_args(message)
    reply = message.reply_to_message
    chat_id = message.chat.id
    media_perm = None
    edit(message, f'`{get_translation("processing")}`')

    try:
        reply_chat = message._client.get_chat(args or chat_id)
        peer = message._client.resolve_peer(args or chat_id)
    except PeerIdInvalid:
        edit(message, f'`{get_translation("groupNotFound")}`')
        return

    if message.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
        perm = message.chat.permissions
        media_perm = perm.can_send_media_messages

    try:
        online_users = message._client.invoke(GetOnlines(peer=peer))
        online = online_users.onlines
    except PeerIdInvalid:
        edit(message, f'`{get_translation("groupNotFound")}`')
        return

    try:
        group_photo = reply_chat.photo.big_file_id
        photo = download_media_wc(group_photo, 'photo.png')
    except BaseException:
        photo = None
        pass

    title = reply_chat.title or get_translation('notSet')
    username = (
        f'**@{reply_chat.username}**'
        if reply_chat.username
        else f'`{get_translation("notFound")}`'
    )
    chat_id = reply_chat.id
    dc_id = reply_chat.dc_id or get_translation('notFound')
    group_type = reply_chat.type
    sticker_pack = (
        f'**[Pack](https://t.me/addstickers/{reply_chat.sticker_set_name})**'
        if reply_chat.sticker_set_name
        else f'`{get_translation("notSet")}`'
    )
    members = reply_chat.members_count
    description = (
        f'\n{reply_chat.description}'
        if reply_chat.description
        else get_translation('notSet')
    )

    caption = get_translation(
        'groupinfoResult',
        [
            '**',
            '`',
            title,
            chat_id,
            dc_id,
            group_type,
            members,
            online,
            sticker_pack,
            username,
            description,
        ],
    )
    if photo and media_perm:
        reply_img(reply or message, photo, caption=caption, delete_file=True)
        message.delete()
    else:
        edit(message, caption, preview=False)


HELP.update({'info': get_translation('groupInfo')})
