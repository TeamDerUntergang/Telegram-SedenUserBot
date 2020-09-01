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

from os import remove, path
from time import sleep
from re import findall
from urllib.parse import quote_plus
from urllib.error import HTTPError
from mimetypes import guess_type
from urbandict import define
from wikipedia import set_lang, summary
from wikipedia.exceptions import DisambiguationError, PageError
from gtts import gTTS
from gtts.lang import tts_langs
from googletrans import LANGUAGES, Translator
from emoji import get_emoji_regexp
from requests import get
from bs4 import BeautifulSoup
from pyrogram import InputMediaPhoto

from sedenbot import KOMUT
from sedenecem.core import (edit, send_log, reply_doc, reply_voice,
                            extract_args, sedenify, get_webdriver)

CARBONLANG = 'auto'
TTS_LANG = 'tr'
TRT_LANG = 'tr'


@sedenify(pattern='^.crblang')
def carbonlang(message):
    global CARBONLANG
    CARBONLANG = extract_args(message)
    edit(message, f'`Karbon modülü için varsayılan dil` **{CARBONLANG}** `olarak ayarlandı.`')


@sedenify(pattern='^.carbon')
def carbon(message):
    match = extract_args(message)
    if len(match) < 1:
        edit(message, '`Komut kullanımı hatalı.`')
        return
    edit(message, '`İşleniyor...`')
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = message.reply_to_message
    pcode = message.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)
    code = quote_plus(pcode)
    edit(message, '`İşleniyor...\nTamamlanma Oranı: 25%`')
    if path.isfile("./carbon.png"):
        remove("./carbon.png")
    url = CARBON.format(code=code, lang=CARBONLANG)
    driver = get_webdriver()
    driver.get(url)
    edit(message, '`İşleniyor...\nTamamlanma Oranı: 50%`')
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_path
        }
    }
    command_result = driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    edit(message, '`İşleniyor...\nTamamlanma Oranı: 75%`')
    while not path.isfile("./carbon.png"):
        sleep(0.5)
    edit(message, '`İşleniyor...\nTamamlanma Oranı: 100%`')
    file = './carbon.png'
    edit(message, '`Resim karşıya yükleniyor...`')
    reply_doc(message, file, caption='Bu resim [Carbon](https://carbon.now.sh/about/) kullanılarak yapıldı,\
        \nbir [Dawn Labs](https://dawnlabs.io/) projesi.', delete_orig=True, delete_after_send=True)
    driver.quit()


# @frknkrc44 tarafından baştan yazıldı
@sedenify(pattern='^.img')
def img(message):
    query = extract_args(message)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
        lim = int(lim)
        if lim > 10:
            lim = 10
    except IndexError:
        lim = 5

    if len(query) < 1:
        edit(message, '`Bir arama terimi girmelisiniz.`')
        return
    edit(message, '`İşleniyor...`')

    url = f'https://www.google.com/search?tbm=isch&q={query}&gbv=2&sa=X&biw=1920&bih=1080'
    driver = get_webdriver()
    driver.get(url)
    count = 1
    files = []
    for i in driver.find_elements_by_xpath('//div[contains(@class,"isv-r PNCib MSM1fd BUooTd")]'):
        i.click()
        try_count = 0
        while len(element := driver.find_elements_by_xpath('//img[contains(@class,"n3VNCb") and contains(@src,"http")]')) < 1 and try_count < 20:
            try_count += 1
            sleep(.1)
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
        except Exception as e:
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
        edit(message, '`Komut kullanımı hatalı.`')
        return
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
        page = int(page)
    except:
        page = 1
    msg = do_gsearch(match, page)
    edit(message, f'**Arama Sorgusu:**\n`{match}`\n\n**Sonuçlar:**\n{msg}', preview=False)

    send_log(f"{match} `sözcüğü başarıyla Google'da aratıldı!`")


def do_gsearch(query, page):

    def find_page(num):
        return (num - 1) * 10;

    def parse_key(keywords):
        return keywords.replace(' ', '+')

    def get_result(res):
        link = res.find('a')['href']
        title = res.find('h3').text
        desc = res.find('span', {'class':['st']}).text
        if len(desc.strip()) < 1:
            desc = 'Açıklama bulunamadı.'
        return f'[{title}]({link})\n`{desc}`'

    query = parse_key(query)
    page = find_page(page)
    req = get(f'https://www.google.com/search?q={query}&start={find_page(page)}',
              headers={
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                  'Content-Type': 'text/html'})
    soup = BeautifulSoup(req.text, 'html.parser')
    res1 = soup.findAll('div', {'class':['rc']})
    out = ""
    for i in range(0, len(res1)):
        res = res1[i]
        out += f"{i+1}-{get_result(res)}\n\n"

    return out


@sedenify(pattern='^.d(uckduck|d)go')
def ddgo(message):
    query = extract_args(message)
    if len(query) < 1:
        edit(message, '`Komut kullanımı hatalı.`')
        return
    req = get(f'https://duckduckgo.com/lite?q={query}',
              headers={
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                  'Content-Type': 'text/html'})
    soup = BeautifulSoup(req.text, 'html.parser')
    res1 = soup.findAll('table', {'border':0})
    res1 = res1[-1].findAll('tr')

    edit(message,
         f'**Arama Sorgusu:**\n`{query}`\n\n'
         f'**Sonuçlar:**\n{do_ddsearch(query, res1)}',
         preview=False)

    send_log(f"{query} `sözcüğü başarıyla DuckDuckGo'da aratıldı!`")


def do_ddsearch(query, res1):
    def splitter(res):
        subs = []
        tlist = None
        comp = False
        for i in range(len(res)):
            item = res[i]
            if res3 := item.find('a', {'class':['result-link']}):
                if comp:
                    subs.append(tlist)
                comp = True
                tlist = []
                tlist.append(res3)
            elif res4 := item.find('td', {'class':['result-snippet']}):
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
        desc = (item[1].text.strip()
                if len(item) > 1
                else 'Açıklama sağlanmamış')
        out += (f'{i+1}-[{ltxt}]({link["href"]})\n{desc}\n\n')

    return out


@sedenify(pattern='^.ud')
def urbandictionary(message):
    match = extract_args(message)
    if len(match) < 1:
        edit(message, '`Komut kullanımı hatalı.`')
        return
    edit(message, '`İşleniyor...`')
    query = extract_args(message)
    try:
        define(query)
    except HTTPError:
        edit(message, f'Üzgünüm, **{query}** için hiçbir sonuç bulunamadı.')
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]['def'])
    exalen = sum(len(i) for i in mean[0]['example'])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            edit(message, '`Sonuç çok uzun, dosya yoluyla gönderiliyor...`')
            file = open('urbandictionary.txt', 'w+')
            file.write('Sorgu: ' + query + '\n\nAnlamı: ' + mean[0]['def'] +
                       '\n\n' + 'Örnek: \n' + mean[0]['example'])
            file.close()
            reply_doc(message, 'urbandictionary.txt', caption='`Sonuç çok uzun, dosya yoluyla gönderiliyor...`')
            if path.exists('urbandictionary.txt'):
                remove('urbandictionary.txt')
            message.delete()
            return
        edit(message, '`Sorgu:` **' + query + '**\n\n`Anlamı:` **' +
             mean[0]['def'] + '**\n\n' + '`Örnek:` \n__' +
             mean[0]['example'] + '__')
    else:
        edit(message, query + ' **için hiçbir sonuç bulunamadı**')

    send_log(query + ' `sözcüğünün UrbanDictionary sorgusu başarıyla gerçekleştirildi!`')


@sedenify(pattern=r'^.wiki')
def wiki(message):
    match = extract_args(message)
    if len(match) < 1:
        edit(message, '`Komut kullanımı hatalı.`')
        return
    set_lang('tr')
    match = extract_args(message)
    try:
        summary(match)
    except DisambiguationError as error:
        edit(message, f'Belirsiz bir sayfa bulundu.\n\n{error}')
        return
    except PageError as pageerror:
        edit(message, f'Aradığınız sayfa bulunamadı.\n\n{pageerror}')
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open('wiki.txt', 'w+')
        file.write(result)
        file.close()
        reply_doc(message, 'wiki.txt', caption='`Sonuç çok uzun, dosya yoluyla gönderiliyor...`')
        if path.exists('wiki.txt'):
            remove('wiki.txt')
        return
    edit(message, '**Arama:**\n`' + match + '`\n\n**Sonuç:**\n' + result)

    send_log(f'{match}` teriminin Wikipedia sorgusu başarıyla gerçekleştirildi!`')


@sedenify(pattern=r'^.tts')
def tts(message):
    textx = message.reply_to_message
    ttsx = extract_args(message)
    if ttsx:
        pass
    elif textx:
        ttsx = textx.text
    else:
        edit(message, '`Yazıdan sese çevirmek için bir metin gir.`')
        return

    try:
        gTTS(ttsx, lang=TTS_LANG)
    except AssertionError:
        edit(message,
             'Metin boş.\n'
             'Ön işleme, tokenizasyon ve temizlikten sonra konuşacak hiçbir şey kalmadı.')
        return
    except ValueError:
        edit(message, 'Bu dil henüz desteklenmiyor.')
        return
    except RuntimeError:
        edit(message, 'Dilin sözlüğünü görüntülemede bir hata gerçekleşti.')
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

    send_log('Metin başarıyla sese dönüştürüldü!')


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
        edit(message, '`Bana çevirilecek bir metin ver!`')
        return

    try:
        reply_text = translator.translate(deEmojify(trt), dest=TRT_LANG)
    except ValueError:
        edit(message, 'Ayarlanan hedef dil geçersiz.')
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f'**{source_lan.title()}** dilinden\n**{transl_lan.title()}** diline çevrildi.\n\n`{reply_text.text}`'

    edit(message, reply_text)

    send_log(f'Birkaç {source_lan.title()} kelime az önce {transl_lan.title()} diline çevirildi.')


def deEmojify(inputString):
    return get_emoji_regexp().sub(u'', inputString)


@sedenify(pattern='^.lang')
def lang(message):
    arr = extract_args(message).split(' ', 1)
    util = arr[0].lower()
    arg = arr[1].lower()
    if util == "trt":
        scraper = "Çeviri"
        global TRT_LANG
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            edit(message, f'`Geçersiz dil kodu!`\n`Geçerli dil kodları`:\n\n`{LANGUAGES}`')
            return
    elif util == "tts":
        scraper = "Yazıdan Sese"
        global TTS_LANG
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            edit(message, f'`Geçersiz dil kodu!`\n`Geçerli dil kodları`:\n\n`{LANGUAGES}`')
            return
    edit(message, f'`{scraper} modülü için varsayılan dil {LANG.title()} diline çevirildi.`')

    send_log(f'`{scraper} modülü için varsayılan dil {LANG.title()} diline çevirildi.`')


@sedenify(pattern='^.currency (.*)')
def currency(message):
    input_str = extract_args(message)
    input_sgra = input_str.split(' ')
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = 'https://api.exchangeratesapi.io/latest?base={}'.format(
                currency_from)
            current_response = get(request_url).json()
            if currency_to in current_response['rates']:
                current_rate = float(current_response['rates'][currency_to])
                rebmun = round(number * current_rate, 2)
                edit(message, '{} {} = {} {}'.format(
                    number, currency_from, rebmun, currency_to))
            else:
                edit(message, '`Yazdığın şey uzaylıların kullandığı bir para birimine benziyor, bu yüzden dönüştüremiyorum.`')
        except Exception as e:
            edit(message, str(e))
    else:
        edit(mesasge, '`Sözdizimi hatası.`')
        return


KOMUT.update({
    'img':
    '.img <kelime>\
    \nKullanım: Google üzerinde hızlı bir resim araması yapar ve ilk 5 resmi gösterir.'
})
KOMUT.update({
    'currency':
    '.currency <miktar> <dönüştürülecek birim> <dönüşecek birim>\
    \nKullanım: Belirtilen para miktarlarını dönüştürür.'
})
KOMUT.update({
    'carbon':
    '.carbon <metin>\
    \nKullanım: carbon.now.sh sitesini kullanarak yazdıklarının aşşşşşşırı şekil görünmesini sağlar.\n.crblang <dil> komutuyla varsayılan dilini ayarlayabilirsin.'
})
KOMUT.update({
    'google':
    '.google <kelime>\
    \nKullanım: Hızlı bir Google araması yapar.'
})
KOMUT.update({
    'duckduckgo':
    '.ddgo <kelime>\
    \nKullanım: Hızlı bir DuckDuckGo araması yapar.'
})
KOMUT.update({
    'wiki':
    '.wiki <terim>\
    \nKullanım: Bir Vikipedi araması gerçekleştirir.'
})
KOMUT.update({
    'ud':
    '.ud <terim>\
    \nKullanım: Urban Dictionary araması yapmanın kolay yolu?'
})
KOMUT.update({
    'tts':
    '.tts <metin>\
    \nKullanım: Metni sese dönüştürür.\n.lang tts komutuyla varsayılan dili ayarlayabilirsin. (Türkçe ayarlı geliyor merak etme.)'
})
KOMUT.update({
    'trt':
    '.trt <metin>\
    \nKullanım: Basit bir çeviri modülü.\n.lang trt komutuyla varsayılan dili ayarlayabilirsin. (Türkçe ayarlı geliyor merak etme.)'
})
