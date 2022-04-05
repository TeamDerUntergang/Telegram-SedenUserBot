# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from datetime import datetime
from functools import reduce
from re import DOTALL, sub

from bs4 import BeautifulSoup
from requests import get
from sedenbot import HELP
from sedenecem.core import edit, extract_args, sedenify


@sedenify(pattern='^.ezan(|vakti)')
def ezanvakti(message):
    konum = extract_args(message).lower()
    if len(konum) < 1:
        return edit(message, '`Lütfen komutun yanına bir şehir belirtin.`')

    result = get_result(konum)
    res1 = result.body.findAll('div', {'class': ['body-content']})
    res1 = res1[0].findAll('script')
    res1 = sub(
        r'<script>|</script>|\r|{.*?}|\[.*?\]|\n    ', '', str(res1[0]), flags=DOTALL
    )
    res1 = sub('\n\n', '\n', res1)[:-1].split('\n')

    def get_val(st):
        return [i.split('=')[1].replace('"', '').strip() for i in st[:-1].split(';')]

    res2 = get_val(res1[1])
    res3 = get_val(res1[2])

    vakitler = (
        '**Diyanet Namaz Vakitleri**\n\n'
        + f'📍 **Yer:** `{res2[1]}`\n\n'
        + f'🏙 **İmsak:** `{res3[0]}`\n'
        + f'🌅 **Güneş:** `{res3[1]}`\n'
        + f'🌇 **Öğle:** `{res3[2]}`\n'
        + f'🌆 **İkindi:** `{res3[3]}`\n'
        + f'🌃 **Akşam:** `{res3[4]}`\n'
        + f'🌌 **Yatsı:** `{res3[5]}`'
    )

    edit(message, vakitler)


@sedenify(pattern='^.ramazan')
def ramazan(message):
    konum = extract_args(message).lower()
    if len(konum) < 1:
        return edit(message, '`Lütfen komutun yanına bir şehir belirtin.`')

    result = get_result(konum)
    saat_imsak = (
        result.find('div', {'data-vakit-name': 'imsak'})
        .find('div', {'class': 'tpt-time'})
        .get_text()
    )

    saat_aksam = (
        result.find('div', {'data-vakit-name': 'aksam'})
        .find('div', {'class': 'tpt-time'})
        .get_text()
    )

    saat_yatsi = (
        result.find('div', {'data-vakit-name': 'yatsi'})
        .find('div', {'class': 'tpt-time'})
        .get_text()
    )

    sehir = (
        result.find('table', {'class': 'table vakit-table'})
        .find('caption')
        .get_text()
        .split(' ')[0]
    )

    saatler_yarin = result.find_all('tr')[2]
    aksam_yarin = saatler_yarin.get_text().split('\n')[6]
    yatsi_yarin = saatler_yarin.get_text().split('\n')[7]
    imsak_yarin = saatler_yarin.get_text().split('\n')[2]

    iftar_saat = calculate_time(saat_aksam, aksam_yarin)
    yatsi_saat = calculate_time(saat_yatsi, yatsi_yarin)
    imsak_saat = calculate_time(saat_imsak, imsak_yarin)

    vakitler = (
        '**Diyanet Ramazan Vakitleri**\n\n'
        + f'📍 **Yer:** `{sehir}`\n\n'
        + f'🏙 **Sahur:** `{saat_imsak} ({imsak_saat[0]}s {imsak_saat[1]}dk kaldı)`\n'
        + f'🌃 **İftar:** `{saat_aksam} ({iftar_saat[0]}s {iftar_saat[1]}dk kaldı)`\n'
        + f'🌌 **Teravih:** `{saat_yatsi} ({yatsi_saat[0]}s {yatsi_saat[1]}dk kaldı)`\n\n'
        + '**Hayırlı Ramazanlar**'
    )

    edit(message, vakitler)


def find_loc(konum):
    if konum.isdigit():
        plaka = int(konum)
        if plaka > 0 and plaka < 82:
            return int(sehirler[plaka - 1].split()[2])
        else:
            return -1
    else:
        di = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u'}
        konum = reduce(lambda x, y: x.replace(y, di[y]), di, konum)
        sehir_ad = [s.split()[1].lower() for s in sehirler]
        try:
            index = sehir_ad.index(konum)
            return int(sehirler[index].split()[2])
        except BaseException:
            return -1


def get_result(konum):
    try:
        knum = find_loc(konum)
        if knum < 0:
            raise ValueError
        request = get(f'https://namazvakitleri.diyanet.gov.tr/tr-TR/{knum}')
        return BeautifulSoup(request.content, 'html.parser')
    except TypeError:
        return f'`{konum} için bir bilgi bulunamadı.`'


def calculate_time(saat, yarin_saat):
    now = datetime.now().timestamp()
    now_t = datetime.fromtimestamp(now).strftime('%d.%m.%Y')
    iftar_vakit = datetime.strptime(f'{saat} {now_t}', '%H:%M %d.%m.%Y').timestamp()
    if iftar_vakit < now:
        temp = now + 24 * 60 * 60
        tomorrow = datetime.fromtimestamp(temp).strftime('%d.%m.%Y')
        yarin_iftar = datetime.strptime(
            f'{yarin_saat} {tomorrow}', '%H:%M %d.%m.%Y'
        ).timestamp()
        sonuc = yarin_iftar - now
        kalan_saat, kalan_dk = timedelta(sonuc)
    else:
        sonuc = iftar_vakit - now
        kalan_saat, kalan_dk = timedelta(sonuc)
    return kalan_saat, kalan_dk


def timedelta(time):
    saat = int(time / 3600)
    dakika = int((time % 3600) / 60)
    return saat, dakika


sehirler = [
    '01 Adana 9146',
    '02 Adiyaman 9158',
    '03 Afyonkarahisar 9167',
    '04 Agri 9185',
    '05 Amasya 9198',
    '06 Ankara 9206',
    '07 Antalya 9225',
    '08 Artvin 9246',
    '09 Aydin 9252',
    '10 Balikesir 9270',
    '11 Bilecik 9297',
    '12 Bingol 9303',
    '13 Bitlis 9311',
    '14 Bolu 9315',
    '15 Burdur 9327',
    '16 Bursa 9335',
    '17 Canakkale 9352',
    '18 Cankiri 9359',
    '19 Corum 9370',
    '20 Denizli 9392',
    '21 Diyarbakir 9402',
    '22 Edirne 9419',
    '23 Elazig 9432',
    '24 Erzincan 9440',
    '25 Erzurum 9451',
    '26 Eskisehir 9470',
    '27 Gaziantep 9479',
    '28 Giresun 9494',
    '29 Gumushane 9501',
    '30 Hakkari 9507',
    '31 Hatay 20089',
    '32 Isparta 9528',
    '33 Mersin 9737',
    '34 Istanbul 9541',
    '35 Izmir 9560',
    '36 Kars 9594',
    '37 Kastamonu 9609',
    '38 Kayseri 9620',
    '39 Kirklareli 9638',
    '40 Kirsehir 9646',
    '41 Kocaeli 9654',
    '42 Konya 9676',
    '43 Kutahya 9689',
    '44 Malatya 9703',
    '45 Manisa 9716',
    '46 Kahramanmaras 9577',
    '47 Mardin 9726',
    '48 Mugla 9747',
    '49 Mus 9755',
    '50 Nevsehir 9760',
    '51 Nigde 9766',
    '52 Ordu 9782',
    '53 Rize 9799',
    '54 Sakarya 9807',
    '55 Samsun 9819',
    '56 Siirt 9839',
    '57 Sinop 9847',
    '58 Sivas 9868',
    '59 Tekirdag 9879',
    '60 Tokat 9887',
    '61 Trabzon 9905',
    '62 Tunceli 9914',
    '63 Sanliurfa 9831',
    '64 Usak 9919',
    '65 Van 9930',
    '66 Yozgat 9949',
    '67 Zonguldak 9955',
    '68 Aksaray 9193',
    '69 Bayburt 9295',
    '70 Karaman 9587',
    '71 Kirikkale 9635',
    '72 Batman 9288',
    '73 Sirnak 9854',
    '74 Bartin 9285',
    '75 Ardahan 9238',
    '76 Igdir 9522',
    '77 Yalova 9935',
    '78 Karabuk 9581',
    '79 Kilis 9629',
    '80 Osmaniye 9788',
    '81 Duzce 9414',
]

HELP.update(
    {
        "ezanvakti": ".ezanvakti <şehir> \
    \nKullanım: Belirtilen şehir için namaz vakitlerini gösterir. \
    \nÖrnek: .ezanvakti istanbul \
    \n.ramazan <şehir> \
    \nKullanım: Belirtilen şehir için ramazan vakitlerini gösterir. \
    \nÖrnek: .ramazan istanbul"
    }
)
