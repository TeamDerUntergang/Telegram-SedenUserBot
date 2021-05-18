# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from sedenbot import BLACKLIST, BRAIN, HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_translation,
    reply_img,
    sedenify,
)


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
        username = (
            f'@{reply_user.username}'
            if reply_user.username
            else get_translation('notSet')
        )
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
        sudo = SudoCheck(user_id)
        blacklist = BlacklistCheck(user_id)

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
                bot,
                scam,
                verified,
                chats,
                bio,
                last_seen,
                sudo if sudo else '',
                blacklist if blacklist else '',
            ],
        )

        if photo and media_perm:
            reply_img(reply or message, photo, caption=caption, delete_file=True)
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


def SudoCheck(user_id):
    if user_id in BRAIN:
        return get_translation('sudoCheck')


def BlacklistCheck(user_id):
    if user_id in BLACKLIST:
        return get_translation('blacklistCheck')


HELP.update({'whois': get_translation('whoisInfo')})
