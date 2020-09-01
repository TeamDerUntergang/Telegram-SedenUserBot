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

from sedenbot import KOMUT
from sedenecem.core import edit, sedenify

@sedenify(pattern='.chatid', private=False)
def chatid(message):
    edit(message, 'Grup ID: `' + str(message.chat.id) + '`')

@sedenify(pattern='^.kickme', compat=False, private=False)
def kickme(client, message):
    edit(message, '`Güle Güle ben gidiyorum 🤠`')
    client.leave_chat(message.chat.id, 'me')


KOMUT.update({
    "chat":
    ".chatid\
\nKullanım: Belirlenen grubun ID numarasını verir\
\n\n.kickme\
\nKullanım: Belirlenen gruptan ayrılmanızı sağlar."
})
