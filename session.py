# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from pyrogram import Client

lang = input('Select lang (tr, en): ').lower()

if lang == 'en':
    print('''\nPlease go to my.telegram.org
Login using your Telegram account
Click on API Development Tools
Create a new application, by entering the required details\n''')

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
        lang_code='en',
    )

    with app:
        self = app.get_me()
        session = app.export_session_string()
        out = f'''**Hi [{self.first_name}](tg://user?id={self.id})
\nAPI_ID:** `{API_ID}`
\n**API_HASH:** `{API_HASH}`
\n**SESSION:** `{session}`
\n**NOTE: Don't give your account information to others!**'''
        app.send_message('me', out)
        print('''Session successfully generated!
Please check your Telegram Saved Messages''')


elif lang == 'tr':
    print('''Lütfen my.telegram.org adresine gidin
Telegram hesabınızı kullanarak giriş yapın
API Development Tools kısmına tıklayın
Gerekli ayrıntıları girerek yeni bir uygulama oluşturun\n''')

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
        self = app.get_me()
        session = app.export_session_string()
        out = f'''**Merhaba [{self.first_name}](tg://user?id={self.id})
\nAPI_ID:** `{API_ID}`
\n**API_HASH:** `{API_HASH}`
\n**SESSION:** `{session}`
\n**NOT: Hesap bilgileriniz başkalarına vermeyin!**'''
        app.send_message('me', out)
        print('''Session başarıyla oluşturuldu!
Lütfen Telegram Kayıtlı Mesajlarınızı kontrol edin.''')


else:
    print('\nWhat? Please select en or tr')
