# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from mimetypes import guess_type
from os import path, remove
from random import choice
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
    google_domains,
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
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    edit(message, f'`{get_translation("processing")}\n%`75')
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Content-Type': 'text/html',
        },
    )

    retries = 0
    while req.status_code != 200 and retries < 10:
        retries += 1
        req = get(
            f'https://{choice(google_domains)}{temp}',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
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
    query = extract_args(message)
    if len(query) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    edit(message, f'`{get_translation("processing")}`')
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


@sedenify(pattern='^.wiki')
def wiki(message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    set_lang(SEDEN_LANG)
    try:
        summary(args)
    except DisambiguationError as error:
        edit(message, get_translation('wikiError', [error]))
        return
    except PageError as pageerror:
        edit(message, get_translation('wikiError2', [pageerror]))
        return
    result = summary(args)
    if len(result) >= 4096:
        file = open('wiki.txt', 'w+')
        file.write(result)
        file.close()
        reply_doc(
            message,
            'wiki.txt',
            caption=f'`{get_translation("outputTooLarge")}`',
            delete_after_send=True,
        )
    edit(message, get_translation('sedenQuery', ['**', '`', args, result]))

    send_log(get_translation('wikiLog', ['`', args]))


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
        reply_text = translator.translate(deEmojify(args), dest=TRT_LANG)
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


HELP.update({'img': get_translation('imgInfo')})
HELP.update({'carbon': get_translation('carbonInfo')})
HELP.update({'goolag': get_translation('googleInfo')})
HELP.update({'duckduckgo': get_translation('ddgoInfo')})
HELP.update({'wiki': get_translation('wikiInfo')})
HELP.update({'ud': get_translation('udInfo')})
HELP.update({'translator': get_translation('translatorInfo')})
