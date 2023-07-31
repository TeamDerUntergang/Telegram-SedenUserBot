# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from json import JSONDecodeError, loads
from mimetypes import guess_type
from os import path, remove
from random import choice, randrange
from re import findall, sub
from time import sleep
from traceback import format_exc
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from emoji import demojize
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
from pyrogram import enums
from pyrogram.types import InputMediaPhoto
from requests import RequestException, get, post
from selenium.webdriver.common.by import By

from sedenbot import HELP, SEDEN_LANG
from sedenecem.core import (
    edit,
    extract_args,
    extract_args_split,
    get_translation,
    get_webdriver,
    google_domains,
    reply_doc,
    reply_voice,
    sedenify,
    send_log,
    useragent,
)

CARBONLANG = 'auto'
TTS_LANG = SEDEN_LANG
TRT_LANG = SEDEN_LANG


@sedenify(pattern='^.crblang')
def carbonlang(message):
    global CARBONLANG
    CARBONLANG = extract_args(message)
    edit(message, get_translation('carbonLang', ['**', CARBONLANG]))


@sedenify(pattern='^.carbon')
def carbon(message):
    match = extract_args(message)
    if len(match) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    edit(message, f'`{get_translation("processing")}`')
    reply = message.reply_to_message
    pcode = message.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif reply:
        pcode = str(reply.message)
    code = quote_plus(pcode)
    global CARBONLANG
    CARBON = f'https://carbon.now.sh/?l={CARBONLANG}&code={code}'
    edit(message, f'`{get_translation("processing")}\n%25`')
    if path.isfile('./carbon.png'):
        remove('./carbon.png')
    driver = get_webdriver()
    driver.get(CARBON)
    edit(message, f'`{get_translation("processing")}\n%50`')
    driver.command_executor._commands['send_command'] = (
        'POST',
        '/session/$sessionId/chromium/send_command',
    )
    driver.find_element(By.XPATH, "//button[contains(text(),'Export')]").click()
    edit(message, f'`{get_translation("processing")}\n%75`')
    while not path.isfile('./carbon.png'):
        sleep(0.5)
    edit(message, f'`{get_translation("processing")}\n%100`')
    file = './carbon.png'
    edit(message, f'`{get_translation("carbonUpload")}`')
    reply_doc(
        reply if reply else message,
        file,
        caption=get_translation('carbonResult'),
        delete_after_send=True,
    )
    message.delete()
    driver.quit()


@sedenify(pattern='^.img')
def img(message):
    query = extract_args(message)
    lim = findall(r'lim=\d+', query)
    try:
        lim = lim[0]
        lim = lim.replace('lim=', '')
        query = query.replace('lim=' + lim[0], '')
        lim = int(lim)
        if lim > 10:
            lim = 10
    except IndexError:
        lim = 3

    if len(query) < 1:
        edit(message, f'`{get_translation("imgUsage")}`')
        return
    edit(message, f'`{get_translation("processing")}`')

    url = f'https://{choice(google_domains)}/search?tbm=isch&q={query}&gbv=2&sa=X&biw=1920&bih=1080'
    driver = get_webdriver()
    driver.get(url)
    count = 1
    files = []
    for i in driver.find_elements(
        By.XPATH, '//div[contains(@class,"isv-r PNCib MSM1fd BUooTd")]'
    ):
        i.click()
        try_count = 0
        while (
            len(
                element := driver.find_elements(
                    By.XPATH,
                    '//img[contains(@class,"n3VNCb") and contains(@src,"http")]',
                )
            )
            < 1
            and try_count < 20
        ):
            try_count += 1
            sleep(0.1)
        if len(element) < 1:
            continue
        link = element[0].get_attribute('src')
        filename = f'result_{count}.jpg'
        try:
            with open(filename, 'wb') as result:
                result.write(get(link).content)
            ftype = guess_type(filename)
            if not ftype[0] or ftype[0].split('/')[1] not in ['png', 'jpg', 'jpeg']:
                remove(filename)
                continue
        except Exception:
            continue
        files.append(InputMediaPhoto(filename))
        sleep(1)
        elements = driver.find_elements(By.XPATH, '//a[contains(@class,"hm60ue")]')
        for element in elements:
            element.click()
        count += 1
        if lim < count:
            break
        sleep(1)

    driver.quit()

    reply_doc(message, files, delete_orig=True, delete_after_send=True)


@sedenify(pattern='^.google')
def google(message):
    match = extract_args(message)
    if len(match) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace('page=', '')
        match = match.replace('page=' + page[0], '')
        page = int(page)
    except BaseException:
        page = 1
    msg = do_gsearch(match, page)
    edit(
        message, get_translation('googleResult', ['**', '`', match, msg]), preview=False
    )

    send_log(get_translation('googleLog', [match]))


def do_gsearch(query, page):
    def find_page(num):
        if num < 1:
            num = 1
        return (num - 1) * 10

    def parse_key(keywords):
        return keywords.replace(' ', '+')

    def replacer(st):
        return (
            sub(r'[`\*_]', '', st)
            .replace('\n', ' ')
            .replace('(', '〈')
            .replace(')', '〉')
            .replace('!', 'ⵑ')
            .strip()
        )

    def get_result(res):
        link = res.find('a', href=True)
        title = res.find('h3')
        if title:
            title = title.text
        desc = res.find(
            'div', attrs={'class': ['VwiC3b', 'yXK7lf', 'MUxGbd', 'yDYNvb', 'lyLwlc']}
        )
        if desc:
            desc = desc.text

        if link and title and desc:
            return f'[{replacer(title)}]({link["href"]})\n{desc or ""}'

    query = parse_key(query)
    page = find_page(page)
    temp = f'/search?q={query}&start={find_page(page)}&hl={SEDEN_LANG}'

    req = get(
        f'https://{choice(google_domains)}{temp}',
        headers={
            'User-Agent': useragent(),
            'Content-Type': 'text/html',
        },
    )

    retries = 0
    while req.status_code != 200 and retries < 10:
        retries += 1
        req = get(
            f'https://{choice(google_domains)}{temp}',
            headers={
                'User-Agent': useragent(),
                'Content-Type': 'text/html',
            },
        )

    soup = BeautifulSoup(req.text, 'html.parser')

    res1 = soup.find_all('div', attrs={'class': 'g'})

    out = ''
    count = 0
    for res in res1:
        try:
            result = get_result(res)
            if result:
                count += 1
                out += f'{count} - {result}\n\n'
        except Exception:
            print(format_exc())
            print(res)
            pass

    return out


@sedenify(pattern='^.d(uckduck|d)go')
def ddgo(message):
    query = extract_args(message)
    if len(query) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    req = get(
        f'https://duckduckgo.com/lite?q={query}',
        headers={
            'User-Agent': useragent(),
            'Content-Type': 'text/html',
        },
    )
    soup = BeautifulSoup(req.text, 'html.parser')
    res1 = soup.findAll('table', {'border': 0})
    res1 = res1[-1].findAll('tr')

    match = do_ddsearch(res1)
    edit(
        message,
        get_translation('googleResult', ['**', '`', query, match]),
        preview=False,
    )
    send_log(get_translation('ddgoLog', [query]))


def do_ddsearch(res1):
    def splitter(res):
        subs = []
        tlist = None
        comp = False
        for i in range(len(res)):
            item = res[i]
            if res3 := item.find('a', {'class': ['result-link']}):
                if comp:
                    subs.append(tlist)
                comp = True
                tlist = []
                tlist.append(res3)
            elif res4 := item.find('td', {'class': ['result-snippet']}):
                tlist.append(res4)
                subs.append(tlist)
            if len(subs) > 9:
                break
        return subs

    res1 = splitter(res1)

    out = ''
    for i in range(len(res1)):
        item = res1[i]
        link = item[0]
        ltxt = link.text.replace('|', '-').replace('...', '').strip()
        desc = item[1].text.strip() if len(item) > 1 else get_translation('ddgoDesc')
        out += f'{i+1} - [{ltxt}]({link["href"]})\n{desc}\n\n'

    return out


@sedenify(pattern='^.ud')
def urbandictionary(message):
    query = extract_args(message)
    if len(query) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    edit(message, f'`{get_translation("processing")}`')
    response = get(f'https://api.urbandictionary.com/v0/define?term={query}')
    data = loads(response.text)
    if len(data["list"]):
        item = data['list'][randrange(9)]
        meanlen = item['definition'] + item['example']
        if len(meanlen) >= 4096:
            edit(message, f'`{get_translation("outputTooLarge")}`')
            file = open('urbandictionary.txt', 'w+')
            file.write(
                'Query: '
                + query
                + '\n\nMeaning: '
                + item['definition']
                + '\n\n'
                + 'Örnek: \n'
                + item['example']
            )
            file.close()
            reply_doc(
                message,
                'urbandictionary.txt',
                caption=f'`{get_translation("outputTooLarge")}`',
            )
            if path.exists('urbandictionary.txt'):
                remove('urbandictionary.txt')
            message.delete()
            return
        edit(
            message,
            get_translation(
                'sedenQueryUd',
                ['**', '`', query, item['definition'], item['example']],
            ),
        )
    else:
        edit(message, get_translation('udNoResult', ['**', query]))


@sedenify(pattern='^.wiki')
def wiki(message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    try:
        result = search_wiki(args)
    except BaseException as e:
        raise e

    if len(result) > 4096:
        with open(f'{args}.txt', 'w', encoding='utf-8') as file:
            file.write(result)
        return reply_doc(
            message,
            f'{args}.txt',
            caption=f'`{get_translation("outputTooLarge")}`',
            delete_after_send=True,
        )

    edit(message, get_translation('sedenQuery', ['**', '`', args, result]))
    send_log(get_translation('wikiLog', ['`', args]))


def search_wiki(query):
    url = f'https://{SEDEN_LANG or "en"}.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'titles': query,
        'exsectionformat': 'wiki',
        'explaintext': 1,
    }

    try:
        response = get(url, params=params)
        response.raise_for_status()
        data = loads(response.text)
        pages = data.get('query', {}).get('pages', {})
        result = ''

        for page in pages.values():
            extract = page.get('extract', '')
            result += extract

        if not result:
            result = get_translation('wikiError')

        return result

    except (RequestException, JSONDecodeError) as e:
        print(f'API Error: {e}')
        return ''


@sedenify(pattern='^.tts')
def text_to_speech(message):
    reply = message.reply_to_message
    args = extract_args(message)
    if args:
        pass
    elif reply:
        if not reply.text:
            return edit(message, f'`{get_translation("ttsUsage")}`')
        args = reply.text
    else:
        edit(message, f'`{get_translation("ttsUsage")}`')
        return

    try:
        gTTS(args, lang=TTS_LANG)
    except AssertionError:
        edit(message, f'`{get_translation("ttsBlank")}`')
        return
    except ValueError:
        edit(message, f'`{get_translation("ttsNoSupport")}`')
        return
    except RuntimeError:
        edit(message, f'`{get_translation("ttsError")}`')
        return
    tts = gTTS(args, lang=TTS_LANG)
    tts.save('h.mp3')
    with open('h.mp3', 'rb') as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(args, lang=TTS_LANG)
        tts.save('h.mp3')
    with open('h.mp3', 'r'):
        reply_voice(reply if reply else message, 'h.mp3', delete_file=True)

    message.delete()
    send_log(get_translation('ttsLog'))


@sedenify(pattern='^.trt')
def translate(message):
    translator = Translator()
    reply = message.reply_to_message
    args = extract_args(message)
    if args:
        pass
    elif reply:
        if not reply.text:
            return edit(message, f'`{get_translation("trtUsage")}`')
        args = reply.text
    else:
        edit(message, f'`{get_translation("trtUsage")}`')
        return

    try:
        reply_text = translator.translate(demojize(args), dest=TRT_LANG)
    except ValueError:
        edit(message, f'`{get_translation("trtError")}`')
        return

    source_lan = LANGUAGES[reply_text.src.lower()]
    transl_lan = LANGUAGES[reply_text.dest.lower()]
    reply_text = '{}\n{}'.format(
        get_translation(
            'transHeader', ['**', '`', source_lan.title(), transl_lan.title()]
        ),
        reply_text.text,
    )

    edit(message, reply_text)

    send_log(get_translation('trtLog', [source_lan.title(), transl_lan.title()]))


@sedenify(pattern='^.lang')
def lang(message):
    arr = extract_args_split(message)

    if len(arr) != 2:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    util = arr[0].lower()
    arg = arr[1].lower()
    if util == 'trt':
        scraper = get_translation('scraper1')
        global TRT_LANG
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            edit(message, get_translation('scraperTrt', ['`', LANGUAGES]))
            return
    elif util == 'tts':
        scraper = get_translation('scraper2')
        global TTS_LANG
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            edit(message, get_translation('scraperTts', ['`', tts_langs()]))
            return
    edit(message, get_translation('scraperResult', ['`', scraper, LANG.title()]))

    send_log(get_translation('scraperLog', ['`', scraper, LANG.title()]))


@sedenify(pattern='^.d[oö]viz')
def doviz(message):
    req = get(
        'https://www.doviz.com/',
        headers={'User-Agent': useragent()},
    )
    page = BeautifulSoup(req.content, 'html.parser')
    res = page.find_all('div', {'class': 'item'})
    out = '**Güncel döviz kurları:**\n\n'
    
    for item in res:
        name = item.find('span', {'class': 'name'}).text
        value = item.find('span', {'class': 'value'}).text
        
        rate_elem = item.find('div', {'class': ['change-rate status down', 'change-rate status up']})
        rate_class = rate_elem['class'][-1] if rate_elem else None
        
        changes_emoji = ''
        if rate_class == 'down':
            changes_emoji = '⬇️'
        elif rate_class == 'up':
            changes_emoji = '⬆️'

        if changes_emoji:
            out += f'{changes_emoji} **{name}:** `{value}`\n'
        else:
            out += f'**{name}:** `{value}`\n'
    
    edit(message, out)



@sedenify(pattern='^.imei(|check)')
def imeichecker(message):
    imei = extract_args(message)
    edit(message, f'`{get_translation("processing")}`')
    if len(imei) != 15:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    try:
        while True:
            response = post(
                f"https://m.turkiye.gov.tr/api2.php?p=imei-sorgulama&txtImei={imei}"
            ).json()
            if not response['data']['asyncFinished']:
                continue
            result = response['data']
            break
        _marka = findall(r'Marka:(.+) Model', result['markaModel'])
        _model = findall(r'Model Bilgileri:(.+)', result['markaModel'])
        _pazaradi = findall(r'Pazar Adı:(.+) Marka', result['markaModel'])
        marka = (
            _marka[0].replace(',', '').strip() if _marka else None
        )
        model = (
            _model[0].replace(',', '').strip() if _model else None
        )
        pazaradi = (
            _pazaradi[0].replace(',', '').strip() if _pazaradi else None
        )
        reply_text = f"<b>Sorgu Tarihi:</b> <code>{result['sorguTarihi']}</code>\n\n"
        reply_text += f"<b>IMEI:</b> <code>{result['imei'][:-5]+5*'*'}</code>\n"
        reply_text += f"<b>Durum:</b> <code>{result['durum']}</code>\n"
        reply_text += f"<b>Pazar Adı:</b> <code>{pazaradi}</code>\n" if pazaradi is not None else ""
        reply_text += f"<b>Marka:</b> <code>{marka}</code>\n" if marka is not None else ""
        reply_text += f"<b>Model:</b> <code>{model}</code>\n\n" if model is not None else ""

        edit(message, reply_text, parse=enums.parse_mode.ParseMode.HTML, preview=False)
    except Exception as e:
        raise e


@sedenify(pattern='^.currency')
def currency_convert(message):
    input_str = extract_args(message)
    input_sgra = input_str.split(' ')
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = f'https://www.x-rates.com/calculator/?from={currency_from}&to={currency_to}&amount={number}'
            current_response = get(request_url, headers={'User-Agent': useragent()})
            if current_response.status_code == 200:
                soup = BeautifulSoup(current_response.text, 'html.parser')
                rebmun = soup.find('span', {'class': 'ccOutputRslt'})
                result = rebmun.find('span')
                result.extract()
                edit(message, f'**{number} {currency_from} = {rebmun.text.strip()}**')
            else:
                edit(message, f'`{get_translation("currencyError")}`')
        except Exception as e:
            edit(message, str(e))
    else:
        edit(message, f'`{get_translation("syntaxError")}`')
        return


HELP.update({'img': get_translation('imgInfo')})
HELP.update({'currency': get_translation('currencyInfo')})
HELP.update({'imeicheck': get_translation('imeiInfo')})
HELP.update({'carbon': get_translation('carbonInfo')})
HELP.update({'goolag': get_translation('googleInfo')})
HELP.update({'duckduckgo': get_translation('ddgoInfo')})
HELP.update({'wiki': get_translation('wikiInfo')})
HELP.update({'ud': get_translation('udInfo')})
HELP.update({'translator': get_translation('translatorInfo')})
