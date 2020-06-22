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

from pyrogram import Client

# Copyright (c) @NaytSeyd, @frknkrc44 | 2020
print("""Lütfen my.telegram.org adresine gidin
Telegram hesabınızı kullanarak giriş yapın
API Development Tools kısmına tıklayın
Gerekli ayrıntıları girerek yeni bir uygulama oluşturun""")
API_KEY = int(input('API ID: '))
API_HASH = input('API HASH: ')

app = Client(
    'sedenuserbot',
    api_id = API_KEY,
    api_hash = API_HASH,
    app_version = "Seden v1.0",
    device_model = "Der Untergang",
    system_version = "1.0",
    lang_code = "tr",
)

with app:
    print(app.export_session_string())
