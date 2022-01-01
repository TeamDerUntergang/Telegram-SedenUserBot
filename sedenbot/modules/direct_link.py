# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import JSONDecodeError
from re import findall, sub
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup
from requests import Session, get
from sedenbot import HELP
from sedenecem.core import edit, extract_args, get_translation, get_webdriver, sedenify


@sedenify(pattern=r'^.direct')
def direct(message):
    edit(message, f'`{get_translation("processing")}`')
    textx = message.reply_to_message
    direct = extract_args(message)
    if direct:
        pass
    elif textx:
        direct = textx.text
    else:
        edit(message, f'`{get_translation("directUsage")}`')
        return

    reply = ''

    def check(url, items, starts=False):
        if isinstance(items, str):
            return url.startswith(items) if starts else items in url

        for item in items:
            if url.startswith(item) if starts else item in url:
                return True
        return False

    for link in direct.replace('\n', ' ').split():
        try:
            if not check(link, ['http://', 'https://'], starts=True):
                raise Exception

            result = urlparse(link)
            all([result.scheme, result.netloc, result.path])
        except BaseException:
            reply += f'`{get_translation("directUrlNotFound")}`\n'
            continue
        try:
            if check(link, 'zippyshare.com'):
                reply += zippy_share(link)
            elif check(link, 'yadi.sk'):
                reply += yandex_disk(link)
            elif check(link, 'mediafire.com'):
                reply += mediafire(link)
            elif check(link, 'sourceforge.net'):
                reply += sourceforge(link)
            elif check(link, 'osdn.net'):
                reply += osdn(link)
            elif check(link, 'github.com'):
                reply += github(link)
            elif check(link, 'androidfilehost.com'):
                reply += androidfilehost(link)
            else:
                reply += f'{get_translation("directUrlNotFound", [link])}\n'
        except BaseException:
            reply += f'{get_translation("directError", [link])}\n'
    edit(message, reply, preview=False)


def zippy_share(link: str) -> str:
    reply = ''
    driver = get_webdriver()
    driver.get(link)
    left = driver.find_element_by_xpath('//div[contains(@class, "left")]')
    font = left.find_elements_by_xpath('.//font')
    name = font[2].text
    size = font[4].text
    button = driver.find_element_by_xpath('//a[contains(@id, "dlbutton")]')
    link = button.get_attribute('href')
    reply += '{}\n'.format(get_translation('directZippyLink', [name, size, link]))
    driver.quit()
    return reply


def yandex_disk(link: str) -> str:
    reply = ''
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        dl_url = get(api.format(link)).json()['href']
        name = dl_url.split('filename=')[1].split('&disposition')[0]
        reply += f'[{name}]({dl_url})\n'
    except KeyError:
        reply += f'`{get_translation("yadiskError")}`\n'
        return reply
    return reply


def mediafire(link: str) -> str:
    reply = ''
    page = BeautifulSoup(get(link).content, 'html.parser')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    size = findall(r'\(.*\)', info.text)[0]
    name = page.find('div', {'class': 'filename'}).text
    reply += f'[{name} {size}]({dl_url})\n'
    return reply


def sourceforge(link: str) -> str:
    file_path = findall(r'files(.*)/download', link)[0]
    reply = f"Mirrors for __{file_path.split('/')[-1]}__\n"
    project = findall(r'projects?/(.*?)/files', link)[0]
    mirrors = (
        f'https://sourceforge.net/settings/mirror_choices?'
        f'projectname={project}&filename={file_path}'
    )
    page = BeautifulSoup(get(mirrors).content, 'html.parser')
    info = page.find('ul', {'id': 'mirrorList'}).findAll('li')
    for mirror in info[1:]:
        name = findall(r'\((.*)\)', mirror.text.strip())[0]
        dl_url = (
            f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        )
        reply += f'[{name}]({dl_url}) '
    return reply


def osdn(link: str) -> str:
    osdn_link = 'https://osdn.net'
    page = BeautifulSoup(get(link, allow_redirects=True).content, 'html.parser')
    info = page.find('a', {'class': 'mirror_link'})
    link = unquote(osdn_link + info['href'])
    reply = f"Mirrors for __{link.split('/')[-1]}__\n"
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        name = findall(r'\((.*)\)', data.findAll('td')[-1].text.strip())[0]
        dl_url = sub(r'm=(.*)&f', f'm={mirror}&f', link)
        reply += f'[{name}]({dl_url}) '
    return reply


def github(link: str) -> str:
    reply = ''
    dl_url = ''
    download = get(link, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
    except KeyError:
        reply += f'`{get_translation("urlError")}`\n'
    name = link.split('/')[-1]
    reply += f'[{name}]({dl_url}) '
    return reply


def androidfilehost(link: str) -> str:
    fid = findall(r'\?fid=[0-9]+', link)[0]
    session = Session()
    user_agent = useragent()
    headers = {'user-agent': user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        'origin': 'https://androidfilehost.com',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': user_agent,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-mod-sbb-ctype': 'xhr',
        'accept': '*/*',
        'referer': f'https://androidfilehost.com/?fid={fid}',
        'authority': 'androidfilehost.com',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {'submit': 'submit', 'action': 'getdownloadmirrors', 'fid': f'{fid}'}
    mirrors = None
    reply = f'URL: {link}\n'
    error = f'`{get_translation("mirrorError")}`\n'
    try:
        req = session.post(
            'https://androidfilehost.com/libs/otf/mirrors.otf.php',
            headers=headers,
            data=data,
            cookies=res.cookies,
        )
        mirrors = req.json()['MIRRORS']
    except (JSONDecodeError, TypeError):
        reply += error
    if not mirrors or len(mirrors) < 1:
        reply += error
        return reply
    for item in mirrors:
        name = item['name']
        dl_url = item['url']
        reply += f'[{name}]({dl_url})\n'
    return reply


def useragent():
    req = get('https://user-agents.net/random')
    soup = BeautifulSoup(req.text, 'html.parser')
    agent = soup.find('article')
    if agent:
        agent = agent.find('li')
        if agent:
            return agent.find('a').text.replace('"', '')

    return 'Googlebot/2.1 (+http://www.google.com/bot.html)'


HELP.update({'direct': get_translation('directInfo')})
