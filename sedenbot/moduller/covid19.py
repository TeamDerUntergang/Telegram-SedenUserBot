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

from requests import get
from json import loads

from sedenbot import KOMUT
from sedenecem.core import edit, sedenify

# Copyright (c) @frknkrc44 | 2020
@sedenify(pattern='^.covid(|19)$')
def covid(message):
    try:
        request = get('https://covid19.saglik.gov.tr/covid19api?getir=sondurum')
        result = loads(request.text)
    except: # pylint: disable=W0702
        edit(message, '`Bir hata oluştu.`')
        return

    if len(result) > 0:
        result = result[0]

    def del_dots(res):
        return res.replace('.', '')

    sonuclar = ( '**🇹🇷 Koronavirüs Verileri 🇹🇷**\n' +
                f'\n**Tarih:** {result["tarih"]}\n' +
                 '\n**Toplam**\n' +
                f'**Test:** `{del_dots(result["toplam_test"])}`\n' +
                f'**Vaka:** `{del_dots(result["toplam_vaka"])}`\n' +
                f'**Ölüm:** `{del_dots(result["toplam_vefat"])}`\n' +
                f'**Ağır hasta:** `{del_dots(result["agir_hasta_sayisi"])}`\n' +
                f'**Zatürre:** `%{result["hastalarda_zaturre_oran"]}`\n' +
                f'**İyileşen:** `{del_dots(result["toplam_iyilesen"])}`\n' +
                 '\n**Bugün**\n' +
                f'**Test:** `{del_dots(result["gunluk_test"])}`\n' +
                f'**Vaka:** `{del_dots(result["gunluk_vaka"])}`\n' +
                f'**Ölüm:** `{del_dots(result["gunluk_vefat"])}`\n' +
                f'**İyileşen:** `{del_dots(result["gunluk_iyilesen"])}`')

    edit(message, sonuclar)

KOMUT.update({
    "covid19":
    ".covid \
    \nKullanım: Hem Dünya geneli hem de Türkiye için güncel Covid 19 istatistikleri."
})
