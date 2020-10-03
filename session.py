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

print("""Please go to my.telegram.org
Login using your Telegram account
Click on API Development Tools
Create a new application, by entering the required details""")

API_ID = ''
API_HASH = ''

while not API_ID.isdigit() or len(API_ID) < 5 or len(API_ID) > 7:
    API_ID = input('API ID: ')

API_ID = int(API_ID)

while len(API_HASH) != 32:
    API_HASH = input('API HASH: ')

app = Client(
    'sedenuserbot',
    api_id=API_ID,
    api_hash=API_HASH,
    app_version="Seden UserBot",
    device_model="Der Untergang",
    system_version="1.0",
    lang_code="tr",
)

with app:
    print(app.export_session_string())
