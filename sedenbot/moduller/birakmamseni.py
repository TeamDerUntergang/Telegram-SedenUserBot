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
#

from requests import post

from sedenbot import KOMUT
from sedenecem.events import edit, sedenify

# Copyright (c) @Adem68 | 2020
@sedenify(pattern='^.b[ıi]rakmamseni$')
def birakmamseni(message):
    url = 'https://birakmamseni.org/'
    path = 'api/counter'

    headers = {
        'User-Agent': 'ajax/7.66.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': '{}'.format(url),
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        response = post(url=url + path, headers=headers)
        count = response.json()['counter'].lstrip('0')
    except:
        edit(message, '`Bir hata oluştu.`')
        return

    sonuc = ('**⚫⚪ Bırakmam Seni Kampanyası Verileri ⚫⚪**\n\n' +
             'Şu an itibarıyla **BIRAKMAM SENİ** kampanyası kapsamında ' +
             f'`{count}` 🖤🤍 adet destekte bulunuldu.\n' +
             f'\nHaydi sen de hemen **BÜYÜK BEŞİKTAŞ’IMIZA** 🦅 destek ol !\n' +
             f'\n[https://birakmamseni.org](https://birakmamseni.org/)\n' +
             f'`\n=============================\n`' +
             f'`SMS, Havale/Eft ve Posta Çeki kanalları ile gelen destekler periyodik olarak sayaca eklenmektedir.`\n' +
             f'`=============================`')

    edit(message, sonuc, preview=False)

KOMUT.update({
    "birakmamseni":
    ".birakmamseni \
    \nKullanım: Beşiktaş'ın Bırakmam Seni kampanyasına yapılan destek sayısını göstermektedir."
})
