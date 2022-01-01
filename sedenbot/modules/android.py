# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from datetime import datetime
from json import loads
from re import sub
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from requests import get
from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, sedenify, use_proxy


@sedenify(pattern='^.magisk$')
def magisk(message):
    magisk_dict = {
        'Stable': 'https://raw.githubusercontent.com/topjohnwu/'
        'magisk-files/master/stable.json',
        'Beta': 'https://raw.githubusercontent.com/topjohnwu/'
        'magisk-files/master/beta.json',
        'Canary': 'https://raw.githubusercontent.com/topjohnwu/'
        'magisk-files/master/canary.json',
    }
    releases = f'**{get_translation("magiskReleases")}**\n'
    for name, release_url in magisk_dict.items():
        try:
            data = get(release_url).json()
            releases += f'`{name}:` [APK v{data["magisk"]["version"]}]({data["magisk"]["link"]})\n'
        except BaseException:
            pass
    edit(message, releases, preview=False)


@sedenify(pattern='^.phh')
def phh(message):
    get_phh = get(
        'https://api.github.com/repos/phhusson/treble_experimentations/releases/latest'
    ).json()
    search = extract_args(message)
    releases = '{}\n'.format(
        get_translation(
            'androidPhhHeader', ['`', "{} ".format(search) if len(search) > 0 else ""]
        )
    )
    count = 0
    for i in range(len(get_phh)):
        try:
            name = get_phh['assets'][i]['name']
            if not name.endswith('img.xz'):
                continue
            elif search not in name:
                continue
            count += 1
            url = get_phh['assets'][i]['browser_download_url']
            releases += f'[{name}]({url})\n'
        except IndexError:
            continue

    if count < 1:
        releases = get_translation('phhError', ['`', '**', search])
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
        edit(message, f'`{get_translation("deviceUsage")}`')
        return
    data = loads(
        get(
            'https://raw.githubusercontent.com/androidtrackers/'
            'certified-android-devices/master/by_device.json'
        ).text
    )
    results = data.get(codename)
    if results:
        reply = "{}\n".format(get_translation('deviceSearch', ['**', codename]))
        for item in results:
            reply += get_translation(
                'deviceSearchResultChild',
                ['**', item['brand'], item['name'], item['model']],
            )
    else:
        reply = get_translation('deviceError', ['`', codename])
    edit(message, reply)


@sedenify(pattern=r'^.codename')
def codename(message):
    textx = message.reply_to_message
    arr = extract_args(message)
    brand = arr
    device = arr
    if ' ' in arr:
        args = arr.split(' ', 1)
        brand = args[0].lower()
        device = args[1].lower()
    elif textx:
        brand = textx.text.split(' ')[0]
        device = ' '.join(textx.text.split(' ')[1:])
    else:
        edit(message, f'`{get_translation("codenameUsage")}`')
        return
    data = loads(
        get(
            'https://raw.githubusercontent.com/androidtrackers/'
            'certified-android-devices/master/by_brand.json'
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}
    devices = devices_lower.get(brand)
    if not devices:
        reply = get_translation('codenameError', ['`', device])
    else:
        results = [
            i
            for i in devices
            if device.lower() in i['name'].lower()
            or device.lower() in i['model'].lower()
        ]
        if results:
            reply = f'{get_translation("codenameSearch", ["**", brand, device])}\n'
            if len(results) > 8:
                results = results[:8]
            for item in results:
                reply += get_translation(
                    'codenameSearchResultChild',
                    ['**', item['device'], item['name'], item['model']],
                )
        else:
            reply = get_translation('codenameError', ['`', device])
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
        edit(message, f'`{get_translation("twrpUsage")}`')
        return
    url = get(f'https://dl.twrp.me/{device}/')
    if url.status_code == 404:
        reply = get_translation('twrpError', ['`', device])
        edit(message, reply)
        return
    page = BeautifulSoup(url.content, 'html.parser')
    download = page.find('table').find('tr').find('a')
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find('span', {'class': 'filesize'}).text
    date = page.find('em').text.strip()
    reply = get_translation(
        'twrpResult', ['**', '__', device, dl_file, dl_link, size, date]
    )
    edit(message, reply)


@sedenify(pattern=r'^.o(range|)f(ox|rp)')
def ofox(message):
    if len(args := extract_args(message)) < 1:
        edit(message, f'`{get_translation("ofrpUsage")}`')
        return

    OFOX_REPO = f'{get_translation("ofrpUrl")}'

    edit(message, f'`{get_translation("ofrpConnect")}`')

    releases = ofrp_get_packages(args)

    if len(releases.releases) < 1:
        edit(
            message,
            get_translation('ofrpNotFound', ['`', args, OFOX_REPO]),
            preview=False,
        )
        return

    out = ''

    for release in releases.releases:
        out += f"[{release.version}{' (Beta)' if release.is_beta() else ''}]({release.file_url}) **{release.file_size}**\n"
        out += f"{release.date or get_translation('ofrpErrorDate')}\n\n"

    if len(out) < 1:
        edit(message, f'`{get_translation("ofrpError")}`')
        return

    edit(message, f'**OrangeFox Recovery ({args}):**\n{out}')


@sedenify(pattern=r'^.specs')
def specs(message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, f'`{get_translation("specsUsage")}`')
        return

    proxy = use_proxy(message)
    link = find_device(args, proxy)

    if not link:
        edit(message, f'`{get_translation("specsError")}`')
        return

    req = get(
        link,
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; '
            '+http://www.google.com/bot.html)'
        },
        proxies=proxy,
    )
    soup = BeautifulSoup(req.text, features='html.parser')

    def get_spec(query, key='data-spec', cls='td'):
        try:
            result = soup.find(cls, {key: query.split()}).text.strip()
            result = get_translation('specsError2') if len(result) < 1 else result
            return result
        except BaseException:
            return get_translation('specsError2')

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
    sensors = get_spec('sensors')
    sarus = sub(r'\s\s+', ', ', get_spec('sar-us'))
    sareu = sub(r'\s\s+', ', ', get_spec('sar-eu'))

    edit(
        message,
        get_translation(
            'specsResult',
            [
                '**',
                '`',
                title,
                launch,
                body,
                sarus,
                sareu,
                os,
                cpuname,
                cpuchip,
                gpuname,
                storage,
                stortyp,
                dispsize,
                dispres,
                bcampx,
                bcamft,
                bcamvd,
                fcampx,
                fcamft,
                fcamvd,
                battery,
                wlan,
                bluetooth,
                gps,
                sensors,
                link,
            ],
        ),
    )


def find_device(query, proxy):
    """@frknkrc44, GSMArena üzerinden cihaz bulma"""
    raw_query = query.lower()

    def replace_query(query):
        return urlencode({'sSearch': query})

    query = replace_query(raw_query)
    req = get(
        f'https://www.gsmarena.com/res.php3?{query}',
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; '
            '+http://www.google.com/bot.html)'
        },
        proxies=proxy,
    )
    soup = BeautifulSoup(req.text, features='html.parser')

    if 'Too' in soup.find('title').text:  # GSMArena geçici ban atarsa
        return None

    res = soup.findAll('div', {'class': ['makers']})

    if not res or len(res) < 1:  # hiçbir cihaz bulunamazsa
        return None

    res = res[0].findAll('li')

    for item in res:
        name = str(item.find('span'))
        name = sub('(<|</)span>', '', name)
        if (
            name[name.find('>') + 1 :].lower() == raw_query
            or sub('<br(>|/>)', ' ', name).lower() == raw_query
        ):
            link = f"https://www.gsmarena.com/{item.find('a')['href']}"
            return link
    return None


class OFRPDeviceInfo:
    def __init__(self, json, releases):
        if not json:
            self.releases = []
            return

        self.codename = json['codename']
        self.oem = json['oem_name']
        self.model = json['model_name']
        self.maintainer_name = json['maintainer']['name']
        self.maintainer_username = json['maintainer']['username']
        self.releases = releases


class OFRPRelease:
    def __init__(self, json):
        self.id = json['_id']
        self.type = json['type']
        self.device = json['device_id']

        date = datetime.utcfromtimestamp(int(json['date'])).strftime(
            '%d-%m-%Y %H:%M:%S'
        )

        self.date = date
        self.file_size = '{:,.2f} MB'.format(int(json['size']) / float(1 << 20))
        self.md5 = json['md5']
        self.version = json['version']

        url = f'https://api.orangefox.download/v3/releases/{self.id}'
        res = ofrp_get(url)

        if not res:
            self.file_name = None
            self.file_url = None
            self.changelog = None

        json = loads(res)

        self.file_name = json['filename']
        self.file_url = list(json['mirrors'].values())[0]
        self.changelog = '\n'.join(json['changelog'])

    def is_beta(self):
        return self.type == 'beta'


def ofrp_get(url):
    try:
        head = {
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'ArabyBot (compatible; Mozilla/5.0; GoogleBot; FAST Crawler 6.4; http://www.araby.com;)',
            'Referer': 'https://orangefox.download/en',
        }
        req = get(url, headers=head)
        if '{' not in req.text:
            raise BaseException
        return req.text
    except BaseException:
        return None


def ofrp_get_packages(device):
    url = f'https://api.orangefox.download/v3/devices/get?codename={device}'
    res = ofrp_get(url)

    if not res:
        return []

    json = loads(res)

    if '_id' not in json:
        return OFRPDeviceInfo(None, None)

    url = f'https://api.orangefox.download/v3/releases/?device_id={json["_id"]}'
    res = ofrp_get(url)

    out = []

    json2 = loads(res)
    json2 = json2['data']

    stables = [x for x in json2 if x['type'] == 'stable']
    betas = [x for x in json2 if x['type'] == 'beta']

    if len(stables):
        stable = [OFRPRelease(x) for x in stables]
        out += stable

    if len(betas):
        beta = [OFRPRelease(x) for x in betas]
        out += beta

    return OFRPDeviceInfo(json, out)


HELP.update({'android': get_translation('androidInfo')})
