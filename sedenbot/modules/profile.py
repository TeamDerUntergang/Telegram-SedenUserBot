# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from pyrogram.errors import UsernameOccupied
from pyrogram.api import functions

from sedenbot import KOMUT
from sedenecem.core import (edit, extract_args, sedenify,
                            send_log, get_translation)
# ====================== CONSTANT ===============================
BIO_SUCCESS = "```Biyografi başarıyla değiştirildi.```"

NAME_OK = "```Adın başarıyla değiştirildi.```"
USERNAME_SUCCESS = "```Kullanıcı adın başarıyla değiştirildi.```"
USERNAME_TAKEN = "```Kullanıcı adı müsait değil.```"
# ===============================================================


@sedenify(pattern='^.reserved$', compat=False)
def reserved(client, message):
    sonuc = client.send(functions.channels.GetAdminedPublicChannels())
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

    client.send(functions.account.UpdateProfile(
        first_name=firstname, last_name=lastname))
    edit(message, NAME_OK)


@sedenify(pattern='^.setbio', compat=False)
def setbio(client, message):
    newbio = extract_args(message)
    client.send(functions.account.UpdateProfile(about=newbio))
    edit(message, BIO_SUCCESS)


@sedenify(pattern='^.username', compat=False)
def username(client, message):
    newusername = extract_args(message)
    try:
        client.send(functions.account.UpdateUsername(username=newusername))
        edit(message, USERNAME_SUCCESS)
    except UsernameOccupied:
        edit(message, USERNAME_TAKEN)


@sedenify(pattern="^.block$", compat=False)
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

    send_log(get_translation("pmBlockedLog", [name0, uid]))


@sedenify(pattern="^.unblock$", compat=False)
def unblockpm(client, message):
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            edit(message, f'`{get_translation("cannotUnblockMyself")}`')
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
        client.unblock_user(uid)
        edit(message, f'`{get_translation("pmUnblocked")}`')

        send_log(get_translation("pmUnblockedLog", [name0, replied_user.id]))
    else:
        edit(message, f'`{get_translation("pmUnblockedUsage")}`')


KOMUT.update({"profile": get_translation("profileInfo")})
