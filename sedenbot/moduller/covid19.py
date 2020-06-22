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

from re import sub, DOTALL
from requests import get
from bs4 import BeautifulSoup

from sedenbot import KOMUT
from sedenecem.events import edit, sedenify

# Copyright (c) @frknkrc44 | 2020
@sedenify(pattern='^.(covid|covid19)$')
def covid(message):
    try:
        request = get('https://covid19.saglik.gov.tr/')
        result = BeautifulSoup(request.text, 'html.parser')
    except:
        edit(message, '`Bir hata oluştu.`')
        return
        
    def to_nums(a):
        return [sub('<span class=".*?">|</span>|\r|\n|\s|\.', '', str(s), flags=DOTALL) for s in a]

    res1 = result.body.findAll('ul', {'class':['list-group','list-group-genislik']})
    res2 = to_nums(res1[0].findAll('span', {'class':['']}))
    res3 = to_nums(res1[1].findAll('span', {'class':['buyuk-bilgi-l-sayi','']}))
    
    sonuclar = ("**🇹🇷 Koronavirüs Verileri 🇹🇷**\n" +
        "\n**Toplam**\n" + 
        f"**Test:** `{res2[0]}`\n" + 
        f"**Vaka:** `{res2[1]}`\n" +
        f"**Ölüm:** `{res2[2]}`\n" +
        f"**Y.Bakım:** `{res2[3]}`\n" +
        f"**Entübe:** `{res2[4]}`\n" +
        f"**İyileşen:** `{res2[5]}`\n" +
        f"\n**Bugün**\n" +
        f"**Test:** `{res3[0]}`\n" +
        f"**Vaka:** `{res3[1]}`\n" +
        f"**Ölüm:** `{res3[2]}`\n" +
        f"**İyileşen:** `{res3[3]}`")

    edit(message, sonuclar)

KOMUT.update({
    "covid19":
    ".covid \
    \nKullanım: Hem Dünya geneli hem de Türkiye için güncel Covid 19 istatistikleri."
})
