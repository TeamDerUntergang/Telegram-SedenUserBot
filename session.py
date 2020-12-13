# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from pyrogram import Client

print('''Please go to my.telegram.org
Login using your Telegram account
Click on API Development Tools
Create a new application, by entering the required details''')

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
    app_version='Seden UserBot',
    device_model='DerUntergang',
    system_version='Session',
    lang_code='tr',
)

with app:
    print(app.export_session_string())
