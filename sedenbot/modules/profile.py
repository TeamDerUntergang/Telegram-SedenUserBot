# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove
from pyrogram.errors import UsernameOccupied
from pyrogram.api.functions import channels, account

from sedenbot import KOMUT
from sedenecem.core import (edit, extract_args, sedenify, send_log,
                            get_translation, download_media_wc)
# ====================== CONSTANT ===============================
INVALID_MEDIA = "`Medya geçerli değil.`"
PP_CHANGED = "`Profil resmi başarıyla değiştirildi.`"
PP_ERROR = "`Resim işlenirken bir hata oluştu.`"

BIO_SUCCESS = "`Biyografi başarıyla değiştirildi.`"
NAME_OK = "`Adın başarıyla değiştirildi.`"
USERNAME_SUCCESS = "`Kullanıcı adın başarıyla değiştirildi.`"
USERNAME_TAKEN = "`Kullanıcı adı müsait değil.`"
# ===============================================================


@sedenify(pattern='^.reserved$', compat=False)
def reserved(client, message):
    sonuc = client.send(channels.GetAdminedPublicChannels())
    mesaj = ''
    for channel_obj in sonuc.chats:
        mesaj += f'{channel_obj.title}\n@{channel_obj.username}\n\n'
    edit(message, mesaj)


@sedenify(pattern='^.name', compat=False)
def name(client, message):
    newname = extract_args(message)
    if ' ' not in newname:
        firstname = newname
        lastname = ''
    else:
        namesplit = newname.split(' ', 1)
        firstname = namesplit[0]
        lastname = namesplit[1]

    client.send(account.UpdateProfile(
        first_name=firstname, last_name=lastname))
    edit(message, NAME_OK)


@sedenify(pattern='^.setpfp$', compat=False)
def set_profilepic(client, message):
    reply = message.reply_to_message
    photo = None
    if (reply and reply.media and (reply.photo or (
            reply.document and 'image' in reply.document.mime_type))):
        photo = download_media_wc(reply, file_name='profile_photo.jpg')
    else:
        edit(message, INVALID_MEDIA)

    if photo:
        client.set_profile_photo(photo=photo)
        remove(photo)
        edit(message, PP_CHANGED)
    else:
        edit(message, PP_ERROR)


@sedenify(pattern=r'^.delpfp', compat=False)
def remove_profilepic(client, message):
    group = message.text[8:]
    if group == 'all':
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    count = 0
    for photo in client.iter_profile_photos('me', limit=lim):
        client.delete_profile_photos(photo.file_id)
        count += 1
    edit(message, f'`{count} adet profil fotoğrafı silindi.`')


@sedenify(pattern='^.setbio', compat=False)
def setbio(client, message):
    newbio = extract_args(message)
    client.send(account.UpdateProfile(about=newbio))
    edit(message, BIO_SUCCESS)


@sedenify(pattern='^.username', compat=False)
def username(client, message):
    newusername = extract_args(message)
    try:
        client.send(account.UpdateUsername(username=newusername))
        edit(message, USERNAME_SUCCESS)
    except UsernameOccupied:
        edit(message, USERNAME_TAKEN)


@sedenify(pattern='^.block$', compat=False)
def blockpm(client, message):
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            edit(message, f'`{get_translation("cannotBlockMyself")}`')
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

    client.block_user(uid)

    edit(message, f'`{get_translation("pmBlocked")}`')

    try:
        from sedenecem.sql.pm_permit_sql import dissprove
        dissprove(uid)
    except BaseException:
        pass

    send_log(get_translation('pmBlockedLog', [name0, uid]))


@sedenify(pattern='^.unblock$', compat=False)
def unblockpm(client, message):
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            edit(message, f'`{get_translation("cannotUnblockMyself")}`')
            return
        name0 = str(replied_user.first_name)
        uid = replied_user.id
        client.unblock_user(uid)
        edit(message, f'`{get_translation("pmUnblocked")}`')

        send_log(get_translation('pmUnblockedLog', [name0, replied_user.id]))
    else:
        edit(message, f'`{get_translation("pmUnblockedUsage")}`')


KOMUT.update({'profile': get_translation('profileInfo')})
