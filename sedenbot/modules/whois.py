# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from sedenbot import HELP
from sedenecem.core import (extract_args, sedenify, edit, reply_img,
                            get_translation, download_media_wc)


@sedenify(pattern='^.whois', compat=False)
def who_is(client, message):
    user_info = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("whoisProcess")}`')
    media_perm = True
    if 'group' in message.chat.type:
        perm = message.chat.permissions
        media_perm = perm.can_send_media_messages

    if user_info:
        try:
            reply_user = client.get_users(user_info)
            reply_chat = client.get_chat(user_info)
        except Exception:
            edit(message, f'`{get_translation("whoisError")}`')
            return
    elif reply:
        reply_user = client.get_users(reply.from_user.id)
        reply_chat = client.get_chat(reply.from_user.id)
    else:
        edit(message, f'`{get_translation("whoisError")}`')
        return
    if reply_user or reply_chat is not None:
        try:
            user_photo = reply_user.photo.big_file_id
            photo = download_media_wc(user_photo, 'photo.png')
        except BaseException:
            photo = None
            pass

        first_name = reply_user.first_name or get_translation('notSet')
        last_name = reply_user.last_name or get_translation('notSet')
        username = f'@{reply_user.username}' if reply_user.username else get_translation(
            'notSet')
        user_id = reply_user.id
        photos = client.get_profile_photos_count(user_id)
        dc_id = reply_user.dc_id
        bot = reply_user.is_bot
        scam = reply_user.is_scam
        verified = reply_user.is_verified
        chats = len(client.get_common_chats(user_id))
        bio = reply_chat.bio or get_translation('notSet')
        status = reply_user.status
        last_seen = LastSeen(bot, status)

        caption = get_translation(
            'whoisResult',
            ['**', '`', first_name, last_name, username, user_id, photos,
             dc_id, bot, scam, verified, chats, bio, last_seen])

        if photo and media_perm:
            reply_img(
                message,
                photo,
                caption=caption,
                delete_file=True,
                delete_orig=True)
        else:
            return edit(message, caption)


def LastSeen(bot, status):
    if bot:
        return 'BOT'
    elif status == 'online':
        return get_translation('statusOnline')
    elif status == 'recently':
        return get_translation('statusRecently')
    elif status == 'within_week':
        return get_translation('statusWeek')
    elif status == 'within_month':
        return get_translation('statusMonth')
    elif status == 'long_time_ago':
        return get_translation('statusLong')


HELP.update({'whois': get_translation('whoisInfo')})
