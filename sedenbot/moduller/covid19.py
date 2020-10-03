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
from sedenecem.core import edit, sedenify, get_translation


@sedenify(pattern='^.covid(|19)$')
def covid(message):
    try:
        request = get(
            'https://covid19.saglik.gov.tr/covid19api?getir=sondurum')
        result = loads(request.text)
    except BaseException:
        edit(message, f'`{get_translation("covidError")}`')
        return

    if len(result) > 0:
        result = result[0]

    def del_dots(res):
        return res.replace('.', '')

    sonuclar = (
        f'**{get_translation("covidData")}**\n' +
        f'\n**{get_translation("covidDate")}** {result["tarih"]}\n' +
        f'\n**{get_translation("covidTotal")}**\n' +
        f'**Test:** `{del_dots(result["toplam_test"])}`\n' +
        f'**{get_translation("covidCases")}** `{del_dots(result["toplam_vaka"])}`\n' +
        f'**{get_translation("covidDeaths")}** `{del_dots(result["toplam_vefat"])}`\n' +
        f'**{get_translation("covidSeriouslyill")}** `{del_dots(result["agir_hasta_sayisi"])}`\n' +
        f'**{get_translation("covidPneumonia")}** `%{result["hastalarda_zaturre_oran"]}`\n' +
        f'**{get_translation("covidHealed")}** `{del_dots(result["toplam_iyilesen"])}`\n' +
        f'\n**{get_translation("covidToday")}**\n' +
        f'**Test:** `{del_dots(result["gunluk_test"])}`\n' +
        f'**{get_translation("covidCases")}** `{del_dots(result["gunluk_vaka"])}`\n' +
        f'**{get_translation("covidDeaths")}** `{del_dots(result["gunluk_vefat"])}`\n' +
        f'**{get_translation("covidHealed")}** `{del_dots(result["gunluk_iyilesen"])}`')

    edit(message, sonuclar)


KOMUT.update({"covid19": get_translation("covidInfo")})
