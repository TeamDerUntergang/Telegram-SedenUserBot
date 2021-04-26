# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from mimetypes import guess_type
from os import path, remove
from re import findall, sub
from time import sleep
from traceback import format_exc
from urllib.error import HTTPError
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from emoji import get_emoji_regexp
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
from pyrogram.types import InputMediaPhoto
from requests import get
from sedenbot import HELP, SEDEN_LANG
from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    get_webdriver,
    reply_doc,
    reply_voice,
    sedenify,
    send_log,
)
from urbandict import define
from wikipedia import set_lang, summary
from wikipedia.exceptions import DisambiguationError, PageError

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
    textx = message.reply_to_message
    pcode = message.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)
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
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    edit(message, f'`{get_translation("processing")}\n%`75')
    while not path.isfile('./carbon.png'):
        sleep(0.5)
    edit(message, f'`{get_translation("processing")}\n%100`')
    file = './carbon.png'
    edit(message, f'`{get_translation("carbonUpload")}`')
    reply_doc(
        message,
        file,
        caption=get_translation('carbonResult'),
        delete_orig=True,
        delete_after_send=True,
    )
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

    url = (
        f'https://www.google.com/search?tbm=isch&q={query}&gbv=2&sa=X&biw=1920&bih=1080'
    )
    driver = get_webdriver()
    driver.get(url)
    count = 1
    files = []
    for i in driver.find_elements_by_xpath(
        '//div[contains(@class,"isv-r PNCib MSM1fd BUooTd")]'
    ):
        i.click()
        try_count = 0
        while (
            len(
                element := driver.find_elements_by_xpath(
                    '//img[contains(@class,"n3VNCb") and contains(@src,"http")]'
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
        driver.find_elements_by_xpath('//a[contains(@class,"hm60ue")]')[0].click()
        count += 1
        if lim < count:
            break
        sleep(1)

    driver.quit()

    reply_doc(message, files, delete_orig=True, delete_after_send=True)


@sedenify(pattern=r'^.google')
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

    def link_replacer(link):
        rep = {'(': '%28', ')': '%29', '[': '%5B', ']': '%5D', '%': '½'}
        for i in rep.keys():
            link = link.replace(i, rep[i])
        return link

    def get_result(res):
        link = res.findAll('a', {'class': ['fuLhoc', 'ZWRArf']})[0]
        href = f"https://google.com{link_replacer(link['href'])}"
        title = link.findAll('span', {'class': ['CVA68e', 'qXLe6d']})[0].text
        title = replacer(title)
        desc = res.findAll('span', {'class': ['qXLe6d', 'FrIlee']})[-1].text
        desc = replacer(desc)
        if len(desc.strip()) < 1:
            desc = get_translation('googleDesc')
        return f'[{title}]({href})\n{desc}'

    query = parse_key(query)
    page = find_page(page)
    req = get(
        f'https://www.google.com/search?q={query}&gbv=1&sei=2oR3X4nhGY611fAP_5-EkAw&start={find_page(page)}',
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/2.2-12; Linux)',
            'Content-Type': 'text/html',
        },
    )
    soup = BeautifulSoup(req.text, 'html.parser')
    res1 = soup.findAll('div', {'class': ['ezO2md']})

    def is_right_class(res):
        ret = res.find('span', {'class': ['qXLe6d', 'dXDvrc']})

        if not ret:
            return False

        ret = ret.parent

        return ret.name == 'a' and 'fuLhoc' in ret['class']

    res1 = [res for res in res1 if is_right_class(res)]

    out = ''
    for i in range(0, len(res1)):
        res = res1[i]
        try:
            out += f'{i+1} - {get_result(res)}\n\n'
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
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
            'AppleWebKit/537.36 (KHTML, like Gecko)'
            'Chrome/81.0.4044.138 Safari/537.36',
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
    match = extract_args(message)
    if len(match) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    edit(message, f'`{get_translation("processing")}`')
    query = extract_args(message)
    try:
        define(query)
    except HTTPError:
        edit(message, get_translation('udResult', ['**', query]))
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]['def'])
    exalen = sum(len(i) for i in mean[0]['example'])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            edit(message, f'`{get_translation("outputTooLarge")}`')
            file = open('urbandictionary.txt', 'w+')
            file.write(
                'Query: '
                + query
                + '\n\nMeaning: '
                + mean[0]['def']
                + '\n\n'
                + 'Örnek: \n'
                + mean[0]['example']
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
                'sedenQueryUd', ['**', '`', query, mean[0]['def'], mean[0]['example']]
            ),
        )
    else:
        edit(message, get_translation('udNoResult', ['**', query]))


@sedenify(pattern=r'^.wiki')
def wiki(message):
    match = extract_args(message)
    if len(match) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    set_lang(SEDEN_LANG)
    match = extract_args(message)
    try:
        summary(match)
    except DisambiguationError as error:
        edit(message, get_translation('wikiError', [error]))
        return
    except PageError as pageerror:
        edit(message, get_translation('wikiError2', [pageerror]))
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open('wiki.txt', 'w+')
        file.write(result)
        file.close()
        reply_doc(message, 'wiki.txt', caption=f'`{get_translation("outputTooLarge")}`')
        if path.exists('wiki.txt'):
            remove('wiki.txt')
        return
    edit(message, get_translation('sedenQuery', ['**', '`', match, result]))

    send_log(get_translation('wikiLog', ['`', match]))


@sedenify(pattern=r'^.tts')
def tts(message):
    textx = message.reply_to_message
    ttsx = extract_args(message)
    if ttsx:
        pass
    elif textx:
        ttsx = textx.text
    else:
        edit(message, f'`{get_translation("ttsUsage")}`')
        return

    try:
        gTTS(ttsx, lang=TTS_LANG)
    except AssertionError:
        edit(message, f'`{get_translation("ttsBlank")}`')
        return
    except ValueError:
        edit(message, f'`{get_translation("ttsNoSupport")}`')
        return
    except RuntimeError:
        edit(message, f'{get_translation("ttsError")}')
        return
    tts = gTTS(ttsx, lang=TTS_LANG)
    tts.save('h.mp3')
    with open('h.mp3', 'rb') as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(ttsx, lang=TTS_LANG)
        tts.save('h.mp3')
    with open('h.mp3', 'r'):
        reply_voice(message, 'h.mp3', delete_orig=True)
        remove('h.mp3')

    send_log(get_translation('ttsLog'))


@sedenify(pattern=r'^.trt')
def trt(message):
    translator = Translator()
    textx = message.reply_to_message
    trt = extract_args(message)
    if trt:
        pass
    elif textx:
        trt = textx.text
    else:
        edit(message, f'{get_translation("trtUsage")}')
        return

    try:
        reply_text = translator.translate(deEmojify(trt), dest=TRT_LANG)
    except ValueError:
        edit(message, f'{get_translation("trtError")}')
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = '{}\n\n{}'.format(
        get_translation(
            'transHeader', ['**', '`', source_lan.title(), transl_lan.title()]
        ),
        reply_text.text,
    )

    edit(message, reply_text)

    send_log(get_translation('trtLog', [source_lan.title(), transl_lan.title()]))


def deEmojify(inputString):
    return get_emoji_regexp().sub(u'', inputString)


@sedenify(pattern='^.lang')
def lang(message):
    arr = extract_args(message).split(' ', 1)

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
    page = BeautifulSoup(get('https://www.doviz.com/').content, 'html.parser')
    res = page.find_all('div', {'class', 'item'})
    out = '**Güncel döviz kurları:**\n\n'
    for i in res:
        name = i.find('span', {'class': 'name'}).text
        value = i.find('span', {'class': 'value'}).text
        out += f'`•`  **{name}:** `{value}`\n'
    edit(message, out)


@sedenify(pattern='^.currency')
def currency(message):
    input_str = extract_args(message)
    input_sgra = input_str.split(' ')
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = f'https://api.ratesapi.io/api/latest?base={currency_from}'
            current_response = get(request_url).json()
            if currency_to in current_response['rates']:
                current_rate = float(current_response['rates'][currency_to])
                rebmun = round(number * current_rate, 2)
                edit(message, f'**{number} {currency_from} = {rebmun} {currency_to}**')
            else:
                edit(message, f'`{get_translation("currencyError")}`')
        except Exception as e:
            edit(message, str(e))
    else:
        edit(message, f'`{get_translation("syntaxError")}`')
        return


HELP.update({'img': get_translation('imgInfo')})
HELP.update({'currency': get_translation('currencyInfo')})
HELP.update({'carbon': get_translation('carbonInfo')})
HELP.update({'goolag': get_translation('googleInfo')})
HELP.update({'duckduckgo': get_translation('ddgoInfo')})
HELP.update({'wiki': get_translation('wikiInfo')})
HELP.update({'ud': get_translation('udInfo')})
HELP.update({'tts': get_translation('ttsInfo')})
HELP.update({'trt': get_translation('trtInfo')})
