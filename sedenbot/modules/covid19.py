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
from bs4 import BeautifulSoup
from re import sub

from sedenbot import HELP
from sedenecem.core import edit, sedenify, get_translation

# Copyright (c) @frknkrc44 | 2020


@sedenify(pattern="^.covid(|19)$")
def covid(message):
    try:
        req = get(
            "https://covid19.saglik.gov.tr/",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Referer": "https://covid19.saglik.gov.tr/",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36",
            },
        )

        soup = BeautifulSoup(req.text, "html.parser")
        scripts = soup.find_all("script")
        for script in scripts:
            turejq = str(script)
            if "var sondurumjson" in turejq:
                result = loads(
                    sub(
                        "(<(/|)script(.*)>|\/\/|<!\[CDATA\[|\]\]>|;|var sondurumjson =|\n|\s)",
                        "",
                        turejq,
                    )
                )
                break
    except BaseException:
        edit(message, f'`{get_translation("covidError")}`')
        return

    if len(result) > 0:
        result = result[0]

    def del_dots(res):
        return res.replace(".", "")

    sonuclar = (
        f'**{get_translation("covidData")}**\n'
        + f'\n**{get_translation("covidDate")}** {result["tarih"]}\n'
        + f'\n**{get_translation("covidTotal")}**\n'
        + f'**{get_translation("covidTests")}** `{del_dots(result["toplam_test"])}`\n'
        + f'**{get_translation("covidCases")}** `{del_dots(result["toplam_hasta"])}`\n'
        + f'**{get_translation("covidDeaths")}** `{del_dots(result["toplam_vefat"])}`\n'
        + f'**{get_translation("covidSeriouslyill")}** `{del_dots(result["agir_hasta_sayisi"])}`\n'
        + f'**{get_translation("covidPneumonia")}** `%{result["hastalarda_zaturre_oran"]}`\n'
        + f'**{get_translation("covidHealed")}** `{del_dots(result["toplam_iyilesen"])}`\n'
        + f'\n**{get_translation("covidToday")}**\n'
        + f'**{get_translation("covidTests")}** `{del_dots(result["gunluk_test"])}`\n'
        + f'**{get_translation("covidCases")}** `{del_dots(result["gunluk_vaka"])}`\n'
        + f'**{get_translation("covidPatients")}** `{del_dots(result["gunluk_hasta"])}`\n'
        + f'**{get_translation("covidDeaths")}** `{del_dots(result["gunluk_vefat"])}`\n'
        + f'**{get_translation("covidHealed")}** `{del_dots(result["gunluk_iyilesen"])}`'
    )

    edit(message, sonuclar)


HELP.update({"covid19": get_translation("covidInfo")})
