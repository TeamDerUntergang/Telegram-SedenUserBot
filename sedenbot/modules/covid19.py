# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import loads
from re import sub

from bs4 import BeautifulSoup
from requests import get
from sedenbot import HELP
from sedenecem.core import edit, get_translation, sedenify


@sedenify(pattern='^.covid(|19)$')
def covid(message):
    try:
        req = get(
            'https://covid19.saglik.gov.tr/',
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Referer': 'https://covid19.saglik.gov.tr/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
            },
        )

        soup = BeautifulSoup(req.text, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            turejq = str(script)
            if 'var sondurumjson' in turejq:
                result = loads(
                    sub(
                        '(<(/|)script(.*)>|\/\/|<!\[CDATA\[|\]\]>|;|var sondurumjson =|\n|\s|var haftalikdurumjson(.*))',
                        '',
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
        return empty_check(res.replace('.', ''))

    def empty_check(res):
        return res if len(res.strip()) else 'N/A'

    sonuclar = (
        f'**{get_translation("covidData")}**\n'
        + f'\n**{get_translation("covidDate")}** {result["tarih"]}\n'
        + f'\n**{get_translation("covidTotal")}**\n'
        + f'**{get_translation("covidTests")}** `{del_dots(result["toplam_test"])}`\n'
        + f'**{get_translation("covidCases")}** `{del_dots(result["toplam_hasta"])}`\n'
        + f'**{get_translation("covidDeaths")}** `{del_dots(result["toplam_vefat"])}`\n'
        + f'**{get_translation("covidSeriouslyill")}** `{del_dots(result["agir_hasta_sayisi"])}`\n'
        + f'**{get_translation("covidPneumonia")}** `%{empty_check(result["hastalarda_zaturre_oran"])}`\n'
        + f'**{get_translation("covidHealed")}** `{del_dots(result["toplam_iyilesen"])}`\n'
        + f'\n**{get_translation("covidToday")}**\n'
        + f'**{get_translation("covidTests")}** `{del_dots(result["gunluk_test"])}`\n'
        + f'**{get_translation("covidCases")}** `{del_dots(result["gunluk_vaka"])}`\n'
        + f'**{get_translation("covidPatients")}** `{del_dots(result["gunluk_hasta"])}`\n'
        + f'**{get_translation("covidDeaths")}** `{del_dots(result["gunluk_vefat"])}`\n'
        + f'**{get_translation("covidHealed")}** `{del_dots(result["gunluk_iyilesen"])}`'
    )

    edit(message, sonuclar)


HELP.update({'covid19': get_translation('covidInfo')})
