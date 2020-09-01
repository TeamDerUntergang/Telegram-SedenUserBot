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

from re import sub
from json import loads
from urllib.parse import urlencode
from time import sleep
from bs4 import BeautifulSoup
from requests import get

from sedenbot import KOMUT, VALID_PROXY_URL
from sedenecem.core import edit, extract_args, sedenify, get_webdriver

GITHUB = 'https://github.com'

@sedenify(pattern='^.magisk')
def magisk(message):
    magisk_dict = {
        "Stable":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
        "Beta":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json",
        "Canary (Debug)":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/debug.json"
    }
    releases = '`Güncel Magisk sürümleri:`\n'
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += f'`{name}:` [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | ' \
                    f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | ' \
                    f'[Uninstaller]({data["uninstaller"]["link"]})\n'
    edit(message, releases, preview=False)

@sedenify(pattern=r'^.device')
def device(message):
    textx = message.reply_to_message
    codename = extract_args(message)
    if codename:
        pass
    elif textx:
        codename = textx.text
    else:
        edit(message, '`Kullanım: .device <kod adı> Örnek: .device raphael`')
        return
    data = loads(get('https://raw.githubusercontent.com/androidtrackers/'
                     'certified-android-devices/master/by_device.json').text)
    results = data.get(codename)
    if results:
        reply = f'**{codename} için arama sonuçları**:\n\n'
        for item in results:
            reply += f"**Marka**: {item['brand']}\n" \
                     f"**İsim**: {item['name']}\n" \
                     f"**Model**: {item['model']}\n\n"
    else:
        reply = f'`{codename} cihazı için bilgi bulunamadı!`\n'
    edit(message, reply)

@sedenify(pattern=r'^.codename')
def codename(message):
    textx = message.reply_to_message
    arr = extract_args(message)
    brand = arr
    device = arr
    if " " in arr:
        args = arr.split(' ', 1)
        brand = args[0].lower()
        device = args[1].lower()
    elif textx:
        brand = textx.text.split(' ')[0]
        device = ' '.join(textx.text.split(' ')[1:])
    else:
        edit(message, '`Kullanım: .codename <marka> <cihaz> Örnek: .codename Xiaomi Mi 9T Pro`')
        return
    data = loads(get('https://raw.githubusercontent.com/androidtrackers/'
                     'certified-android-devices/master/by_brand.json').text)
    devices_lower = {k.lower():v for k, v in data.items()}
    devices = devices_lower.get(brand)
    if not devices:
        reply = f'`{device} bulunamadı`\n'
    else:
        results = [i for i in devices if device.lower() in i["name"].lower() or device.lower() in i["model"].lower()]
        if results:
            reply = f'**{brand} {device} için arama sonuçları**:\n\n'
            if len(results) > 8:
                results = results[:8]
            for item in results:
                reply += f"**Kod Adı**: {item['device']}\n" \
                         f"**İsim**: {item['name']}\n" \
                         f"**Model**: {item['model']}\n\n"
        else:
            reply = f"`{device} bulunamadı`\n"
    edit(message, reply)

@sedenify(pattern=r'^.twrp')
def twrp(message):
    textx = message.reply_to_message
    device = extract_args(message)
    if device:
        pass
    elif textx:
        device = textx.text.split(' ')[0]
    else:
        edit(message, '`Kullanım: .twrp <kod adı> Örnek: .twrp raphael`')
        return
    url = get(f'https://dl.twrp.me/{device}/')
    if url.status_code == 404:
        reply = f'`{device} için resmi twrp bulunamadı!`\n'
        edit(message, reply)
        return
    page = BeautifulSoup(url.content, 'html.parser')
    download = page.find('table').find('tr').find('a')
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = f'**{device} için güncel twrp:**\n' \
        f'[{dl_file}]({dl_link}) - __{size}__\n' \
        f'**Güncelleme tarihi:** __{date}__\n'
    edit(message, reply)

@sedenify(pattern=r'^.o(range|)f(ox|rp)')
def ofox(message):
    if len(args := extract_args(message)) < 1:
        edit(message, '`Kullanım: .orangefox <kod adı> Örnek: .orangefox raphael`')
        return


    OFOX_REPO = 'https://orangefox.download/tr-TR'
    OFOX_URL = f'{OFOX_REPO}/device/{args}'

    edit(message, '`OrangeFox sunucularına bağlanılıyor ...`')

    driver = get_webdriver()
    driver.get(OFOX_URL)

    notfound = driver.find_elements_by_xpath('//img[contains(@alt,"Not Found")]')

    if len(notfound) > 0:
        edit(message, f'`{args} kod adı muhtemelen resmi bir cihaza ait değil.` {OFOX_REPO} `adresinden kontrol edebilirsiniz.`', preview=False)
        return

    try:
        beta = driver.find_element_by_xpath('//div[contains(@id, "release-beta-header")]')
        if beta:
            beta.click()
    except:
        pass

    sleep(1)

    ofrp_map = {}

    for i in driver.find_elements_by_xpath('//div[contains(@class, "MuiAccordionDetails-root")]'):
        version = i.find_elements_by_xpath('.//p[contains(@class, "MuiTypography-body1")]')

        if len(version) < 1:
            continue

        clcks = i.find_elements_by_xpath('.//div[contains(@class, "MuiPaper-root MuiAccordion-root jss66 MuiAccordion-rounded MuiPaper-elevation1 MuiPaper-rounded")]')
        lists = i.find_elements_by_xpath('.//li[contains(@class, "MuiListItem-root MuiListItem-gutters")]')
        for g in range(len(version)):
            if g < len(clcks):
                try:
                    clcks[g].click()
                except:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(1)
                    try:
                        clcks[g].click()
                    except:
                        pass

            frow = lists[g*2]
            srow = lists[(g*2)+1]

            while len(name_str := frow.find_elements_by_xpath('.//span[contains(@class, "MuiListItemText-primary")]')) < 1:
                sleep(1)

            # dummy but don't delete
            _ = srow.find_elements_by_xpath('.//p[contains(@class, "MuiListItemText-secondary")]')

            date_str = frow.find_elements_by_xpath('.//p[contains(@class, "MuiListItemText-secondary")]')

            link = f"https://files.orangefox.tech/OrangeFox-{'Stable' if '-Stable-' in name_str else 'Beta'}/{args}/{name_str[0].text}"

            ofrp_map[version[g].text] = [date_str[0].text, link]

    driver.quit()

    out = ''

    for key in ofrp_map.keys():
        item = ofrp_map[key]
        out += f"[{key}{' (Beta)' if not '-Stable-' in item[1] else ''}]({item[1]})\n"
        out += f"{item[0] if len(item[0].strip()) > 0 else 'Tarih bilgisi çekilemedi'}\n\n"

    if len(out) < 1:
        edit(message, '`Muhtemelen bu liste boş.`')
        return

    edit(message, f'**OrangeFox Recovery ({args}):**\n{out}')

# Copyright (c) @frknkrc44 | 2020
@sedenify(pattern=r'^.specs')
def specs(message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, '`Kullanım: .specs <cihaz>`')
        return

    edit(message, '`Proxy getiriliyor ...`')
    proxy = get_random_proxy()
    edit(message, '`Proxy bağlantısı sağlanıyor ...`')
    link = find_device(args, proxy)

    if not link:
        edit(message, '`Bu cihaza dair bir bilgi bulunamadı veya '
                      'çok fazla istek attınız.`')
        return

    req = get(link,
              {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; '
                            '+http://www.google.com/bot.html)'},
              proxies=proxy)
    soup = BeautifulSoup(req.text, features='html.parser')

    def get_spec(query, key='data-spec', cls='td'):
        try:
            result = soup.find(cls, {key:query.split()}).text.strip()
            result = "Bilgi alınamadı" if len(result) < 1 else result
            return result
        except:
            return "Bilgi alınamadı"

    title = get_spec('specs-phone-name-title', 'class', 'h1')
    launch = get_spec('released-hl', cls='span')
    body = sub(', ', 'g, ', get_spec('body-hl', cls='span'))
    os = get_spec('os-hl', cls='span')
    storage = get_spec('internalmemory')
    stortyp = get_spec('memoryother')
    dispsize = get_spec('displaysize-hl', cls='span')
    dispres = get_spec('displayres-hl', cls='div')
    bcampx = get_spec('cam1modules')
    bcamft = get_spec('cam1features')
    bcamvd = get_spec('cam1video')
    fcampx = get_spec('cam2modules')
    fcamft = get_spec('cam2features')
    fcamvd = get_spec('cam2video')
    cpuname = get_spec('chipset')
    cpuchip = get_spec('cpu')
    gpuname = get_spec('gpu')
    battery = get_spec('batdescription1')
    wlan = get_spec('wlan')
    bluetooth = get_spec('bluetooth')
    gps = get_spec('gps')
    usb = get_spec('usb')
    sensors = get_spec('sensors')
    sarus = sub(r'\s\s+', ', ', get_spec('sar-us'))
    sareu = sub(r'\s\s+', ', ', get_spec('sar-eu'))

    edit(message, f'**{title}**\n\n'
                  f'**Çıkış tarihi:** `{launch}\n`'
                  f'**Ağırlık ve kalınlık:** `{body}`\n'
                  f'**SAR değeri (ABD):** `{sarus}`\n'
                  f'**SAR değeri (Avr):** `{sareu}`\n'
                  f'**İşletim sistemi:** `{os}`\n'
                  f'**İşlemci:** `{cpuname}`\n'
                  f'**İşlemci çekirdekleri:** `{cpuchip}`\n'
                  f'**Grafik işlemci:** `{gpuname}`\n'
                  f'**Bellek:** `{storage}\n`'
                  f'**Bellek tipi:** `{stortyp}`\n'
                  f'**Ekran boyutu:** `{dispsize}`\n'
                  f'**Ekran çözünürlüğü:** `{dispres}`\n'
                  f'**Arka kamera(lar):**\n`{bcampx}`\n'
                  f'**Arka kamera özellikleri:** `{bcamft}`\n'
                  f'**Arka kamera video kaydı:** `{bcamvd}`\n'
                  f'**Ön kamera(lar):**\n`{fcampx}`\n'
                  f'**Ön kamera özellikleri:** `{fcamft}`\n'
                  f'**Ön kamera video kaydı:** `{fcamvd}`\n'
                  f'**Pil:** `{battery}`\n'
                  f'**Kablosuz:** `{wlan}`\n'
                  f'**Bluetooth:** `{bluetooth}`\n'
                  f'**GPS:** `{gps}`\n'
                  f'**Sensörler:** `{sensors}`\n'
                  f'\nDaha fazlası için: {link}')

# @frknkrc44, GSMArena üzerinden cihaz bulma
def find_device(query, proxy):
    raw_query = query.lower()

    def replace_query(query):
        return urlencode({'sSearch':query})

    query = replace_query(raw_query)
    req = get(f"https://www.gsmarena.com/res.php3?{query}",
              {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; '
                            '+http://www.google.com/bot.html)'},
              proxies=proxy)
    soup = BeautifulSoup(req.text, features='html.parser')

    if 'Too' in soup.find('title').text: # GSMArena geçici ban atarsa
        return None

    res = soup.findAll('div', {'class':['makers']})

    if not res or len(res) < 1: # hiçbir cihaz bulunamazsa
        return None

    res = res[0].findAll('li')

    for item in res:
        name = str(item.find('span'))
        name = sub('(<|</)span>', '', name)
        if name[name.find('>')+1:].lower() == raw_query or sub('<br(>|/>)', ' ', name).lower() == raw_query:
            link = f"https://www.gsmarena.com/{item.find('a')['href']}"
            return link
    return None

def _xget_random_proxy():
    try_valid = tuple(VALID_PROXY_URL[0].split(':')) if len(VALID_PROXY_URL) > 0 else None
    if try_valid:
        valid = _try_proxy(try_valid)
        if valid[0] == 200 and "<title>Too" not in valid[1]:
            return try_valid

    head = {
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"en-US,en;q=0.8",
        "User-Agent":"ArabyBot (compatible; Mozilla/5.0; GoogleBot; FAST Crawler 6.4; http://www.araby.com;)",
        "Referer":"https://www.google.com/search?q=sslproxies",
    }

    req = get('https://sslproxies.org/', head)
    soup = BeautifulSoup(req.text, 'html.parser')
    res = soup.find('table', {'id':'proxylisttable'}).find('tbody')
    res = res.findAll('tr')
    for item in res:
        infos = item.findAll('td')
        ip = infos[0].text
        port = infos[1].text
        proxy = (ip, port)
        if _try_proxy(proxy)[0] == 200:
            return proxy

    return None


def _try_proxy(proxy):
    try:
        prxy = f"{proxy[0]}:{proxy[1]}"
        req = get('https://www.gsmarena.com/', proxies={"http":prxy, "https":prxy}, timeout=1)
        if req.status_code == 200:
            return (200, req.text)
        raise Exception
    except:
        return (404, None)


def get_random_proxy():
    proxy = _xget_random_proxy()
    proxy = f"{proxy[0]}:{proxy[1]}"
    VALID_PROXY_URL.clear()
    VALID_PROXY_URL.append(proxy)

    proxy_dict = {
        "https": proxy,
    }

    return proxy_dict

KOMUT.update({
    "android":
    ".magisk\
\nGüncel Magisk sürümleri\
\n\n.device <kod adı>\
\nKullanım: Android cihazı hakkında bilgi\
\n\n.codename <marka> <cihaz>\
\nKullanım: Android cihaz kod adlarını arayın.\
\n\n.specs <marka> <cihaz>\
\nKullanım: Cihaz özellikleri hakkında bilgi alın.\
\n\n.twrp <kod adı>\
\nKullanım: Hedeflenen cihaz için resmi olan güncel TWRP sürümlerini alın.\
\n\n.orangefox <kod adı>\
\nKullanım: Hedeflenen cihaz için resmi olan güncel OrangeFox Recovery sürümlerini alın."
})
