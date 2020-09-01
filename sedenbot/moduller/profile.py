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
from sedenecem.core import edit, extract_args, sedenify
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

    client.send(functions.account.UpdateProfile(first_name=firstname, last_name=lastname))
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


KOMUT.update({
    "profile":
    ".username <yeni kullanıcı adı>\
\nKullanımı: Telegram'daki kullanıcı adınızı değişir.\
\n\n.name <isim> or .name <isim> <soyisim>\
\nKullanımı: Telegram'daki isminizi değişir. (Ad ve soyad ilk boşluğa dayanarak birleştirilir.)\
\n\n.setbio <yeni biyografi>\
\nKullanımı: Telegram'daki biyografinizi bu komutu kullanarak değiştirin..\
\n\n.reserved\
\nKullanımı: Rezerve ettiğiniz kullanıcı adlarını gösterir."
})
