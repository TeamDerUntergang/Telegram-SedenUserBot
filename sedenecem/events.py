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

from pyrogram import Client, Filters, MessageHandler, Chat
from sedenbot.seden_main import app
from sedenbot import SUPPORT_GROUP, LOG_ID, BLACKLIST, BRAIN_CHECKER, CHROME_DRIVER, me
from re import sub
from time import gmtime, strftime
from subprocess import Popen, PIPE
from os import execl, remove
from math import floor
from traceback import format_exc
import sys
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from PIL import Image

MARKDOWN_FIX_CHAR = '\u2064'

# Copyright (c) @NaytSeyd, @frknkrc44 | 2020
def sedenify(**args):
    pattern = args.get('pattern', None)
    outgoing = args.get('outgoing', True)
    incoming = args.get('incoming', False)
    disable_edited = args.get('disable_edited', False)
    compat = args.get('compat', True)
    brain = args.get('brain', False)
    private = args.get('private', True)
    group = args.get('group', True)

    if pattern and '.' in pattern[:2]:
        args['pattern'] = pattern = pattern.replace('.','[.?]')

    def msg_decorator(func):
        def wrap(client, message):
            try:
                if len(me) < 1:
                    me.append(app.get_me())

                    if me[0].id in BLACKLIST:
                        raise RetardsException('RETARDS CANNOT USE THIS BOT')

                if message.chat.type == 'channel':
                    return

                if not private and message.chat.type in ['private', 'bot']:
                    edit(message, '`Bu komut sadece gruplarda kullanılabilir.`')
                    return

                if not group and message.chat.type in ['group', 'supergroup']:
                    edit(message, '`Bu komut sadece özelde kullanılabilir.`')
                    return

                if not compat:
                    func(client, message)
                else:
                    func(message)
            except RetardsException:
                try:
                    app.disconnect()
                    app.terminate()
                except:
                    pass
                execl(sys.executable, 'killall', sys.executable)
            except Exception as e:
                try:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    if '.crash' == f'{message.text}':
                        text = 'Bu bir test raporudur, LOG_ID kontrolü içindir.'
                    else:
                        edit(message, '`Bir sorun oluştu, kayıtları log grubundan gönderiyorum ...`')
                        link = f'[Seden Destek Grubu](https://telegram.dog/{SUPPORT_GROUP})'
                        text = ('**SEDENBOT HATA RAPORU**\n'
                                'İsterseniz, bunu rapor edebilirsiniz '
                               f'- sadece bu mesajı buraya iletin {link}.\n'
                                'Hata ve Tarih dışında hiçbir şey kaydedilmez\n')

                    ftext = ('========== UYARI =========='
                             '\nBu dosya sadece burada yüklendi,'
                             '\nsadece hata ve tarih kısmını kaydettik,'
                             '\ngizliliğinize saygı duyuyoruz,'
                             '\nburada herhangi bir gizli veri varsa'
                             '\nbu hata raporu olmayabilir, kimse verilerinize ulaşamaz.\n'
                             '================================\n\n'
                             '--------SEDENBOT HATA GUNLUGU--------\n'
                            f'\nTarih: {date}'
                            f'\nGrup ID: {message.chat.id}'
                            f'\nGönderen kişinin ID: {message.from_user.id}'
                            f'\n\nOlay Tetikleyici:\n{message.text}'
                            f'\n\nGeri izleme bilgisi:\n{format_exc()}'
                            f'\n\nHata metni:\n{sys.exc_info()[1]}'
                             '\n\n--------SEDENBOT HATA GUNLUGU BITIS--------'
                             '\n\n\nSon 10 commit:\n')

                    process = Popen(['git','log', '--pretty=format:"%an: %s"', '-10'], stdout=PIPE, stderr=PIPE)
                    out, err = process.communicate()
                    out = f'{out.decode()}\n{err.decode()}'.strip()

                    ftext += out

                    file = open('hata.log', 'w+')
                    file.write(ftext)
                    file.close()

                    send_log_doc('hata.log', caption=text, remove_file=True)
                    raise e
                except Exception as x:
                    raise x

        filter = None
        if pattern:
            filter = Filters.regex(pattern)
            if brain:
                filter &= Filters.user(BRAIN_CHECKER)
            if outgoing and not incoming:
                filter &= Filters.me
            elif incoming and not outgoing:
                filter &= (Filters.incoming & ~Filters.bot)
        else:
            if outgoing and not incoming:
                filter = Filters.me
            elif incoming and not outgoing:
                filter = (Filters.incoming & ~Filters.bot)
            else:
                filter = (Filters.me | Filters.incoming) & ~Filters.bot

        if disable_edited:
            filter &= ~Filters.edited

        app.add_handler(MessageHandler(wrap, filter))

    return msg_decorator


def extract_args(message, markdown=True):
    text = message.text.markdown if markdown else message.text
    if not ' ' in text:
        return ''

    text = sub('\s+',' ',text)
    text = text[text.find(' '):].strip()
    return text


def extract_args_arr(message, markdown=True):
    return extract_args(message, markdown).split()


def edit(message, text, preview=True, fix_markdown=False, parse='md'):
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        if message.from_user.id != me[0].id:
            reply(message, text, preview=preview, parse=parse)
            return
        message.edit_text(text.strip(), disable_web_page_preview=not preview, parse_mode=parse)
    except:
        pass


def reply(message, text, preview=True, fix_markdown=False, delete_orig=False, parse='md'):
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        message.reply_text(text.strip(), disable_web_page_preview=not preview, parse_mode=parse)
        if delete_orig:
            message.delete()
    except:
        pass


def reply_img(message, photo, caption='', fix_markdown=False, delete_orig=False, delete_file=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        message.reply_photo(photo, caption=caption.strip())
        if delete_orig:
            message.delete()

        if delete_file:
            remove(photo)
    except:
        pass


def reply_audio(message, audio, caption='', fix_markdown=False, delete_orig=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        message.reply_audio(audio, caption=caption.strip())
        if delete_orig:
            message.delete()
    except:
        pass


def reply_voice(message, voice, caption='', fix_markdown=False, delete_orig=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        message.reply_voice(voice, caption=caption.strip())
        if delete_orig:
            message.delete()
    except:
        pass


def reply_doc(message, doc, caption='', fix_markdown=False, delete_orig=False, progress=None, delete_after_send=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        if isinstance(doc, str):
            message.reply_document(doc, caption=caption.strip(), progress=progress)
            if delete_after_send:
                remove(doc)
        else:
            message.reply_media_group(doc)
            if delete_after_send:
                for media in doc:
                    remove(media.media)
        if delete_orig:
            message.delete()
    except Exception as e:
        raise e


def reply_sticker(message, sticker, delete_orig=False):
    try:
        message.reply_sticker(sticker)
        if delete_orig:
            message.delete()
    except:
        pass


def send_log(text, fix_markdown=False):
    send(app, LOG_ID if LOG_ID else get_me().id, text, fix_markdown=fix_markdown)


def send_log_doc(doc, caption='', fix_markdown=False, remove_file=False):
    send_doc(app, LOG_ID if LOG_ID else get_me().id, doc, caption=caption, fix_markdown=fix_markdown)
    if remove_file:
        remove(doc)


def get_me():
    return app.get_me()


def send(client, chat, text, fix_markdown=False, reply_id=None):
    if fix_markdown:
        text += MARKDOWN_FIX_CHAR

    if len(text) < 4096:
        if not reply_id:
            client.send_message(chat.id if isinstance(chat, Chat) else chat, text)
        else:
            client.send_message(chat.id if isinstance(chat, Chat) else chat, text, reply_to_message_id=reply_id)
        return

    file = open('temp.txt', 'w+')
    file.write(text)
    file.close()
    send_doc(client, chat, 'temp.txt')


def send_doc(client, chat, doc, caption='', fix_markdown=False):
    if len(caption) > 0 and fix_markdown:
        caption += MARKDOWN_FIX_CHAR
    client.send_document(chat if isinstance(chat, int) else chat.id, doc, caption=caption)


def download_media(client, data, file_name=None, progress=None):
    if not file_name:
        if data.document:
            file_name = (data.document.file_name
                         if data.document.file_name
                         else f'{data.document.file_id}.bin')
        elif data.audio:
            file_name = (data.audio.file_name
                         if data.audio.file_name
                         else f'{data.audio.file_id}.mp3')
        elif data.photo:
            file_name = f'{data.photo.file_id}.png'
        elif data.voice:
            file_name = f'{data.voice.file_id}.ogg'
        elif data.video:
            file_name = (data.video.file_name
                         if data.video.file_name
                         else f'{data.video.file_id}.mp4')
        elif data.animation:
            file_name = f'{data.animation.file_id}.mp4'
        elif data.video_note:
            file_name = f'{data.video_note.file_id}.mp4'
        elif data.sticker:
            file_name = f'{data.sticker.file_id}.{"tgs" if data.sticker.is_animated else "png"}'
        else:
            return None

    if progress:
        return client.download_media(data, file_name=file_name, progress=progress)
    
    return client.download_media(data, file_name=file_name)


def download_media_wc(data, file_name=None, progress=None):
    return download_media(app, data, file_name, progress)


def get_webdriver():
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    prefs = {'download.default_directory': './'}
    options.add_experimental_option('prefs', prefs)
    return Chrome(executable_path=CHROME_DRIVER, options=options)


def sticker_resize(photo):
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = floor(size1new)
        size2new = floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)

    temp = 'temp.png'
    image.save(temp, 'PNG')
    return temp


class RetardsException(Exception):
    pass
