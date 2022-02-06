# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import makedirs
from re import escape, sub
from subprocess import CalledProcessError, check_output, STDOUT

from pyrogram.types import Message
from sedenbot import BOT_PREFIX, BRAIN, LOG_VERBOSE, TEMP_SETTINGS, app

MARKDOWN_FIX_CHAR = '\u2064'
SPAM_COUNT = [0]
_parsed_prefix = escape(BOT_PREFIX) if BOT_PREFIX else r'\.'
_admin_status_list = ['creator', 'administrator']
google_domains = [
    'www.google.com',
    'www.google.ad',
    'www.google.ae',
    'www.google.com.af',
    'www.google.com.ag',
    'www.google.com.ai',
    'www.google.am',
    'www.google.co.ao',
    'www.google.com.ar',
    'www.google.as',
    'www.google.at',
    'www.google.com.au',
    'www.google.az',
    'www.google.ba',
    'www.google.com.bd',
    'www.google.be',
    'www.google.bf',
    'www.google.bg',
    'www.google.com.bh',
    'www.google.bi',
    'www.google.bj',
    'www.google.com.bn',
    'www.google.com.bo',
    'www.google.com.br',
    'www.google.bs',
    'www.google.co.bw',
    'www.google.by',
    'www.google.com.bz',
    'www.google.ca',
    'www.google.cd',
    'www.google.cf',
    'www.google.cg',
    'www.google.ch',
    'www.google.ci',
    'www.google.co.ck',
    'www.google.cl',
    'www.google.cm',
    'www.google.cn',
    'www.google.com.co',
    'www.google.co.cr',
    'www.google.com.cu',
    'www.google.cv',
    'www.google.com.cy',
    'www.google.cz',
    'www.google.de',
    'www.google.dj',
    'www.google.dk',
    'www.google.dm',
    'www.google.com.do',
    'www.google.dz',
    'www.google.com.ec',
    'www.google.ee',
    'www.google.com.eg',
    'www.google.es',
    'www.google.com.et',
    'www.google.fi',
    'www.google.com.fj',
    'www.google.fm',
    'www.google.fr',
    'www.google.ga',
    'www.google.ge',
    'www.google.gg',
    'www.google.com.gh',
    'www.google.com.gi',
    'www.google.gl',
    'www.google.gm',
    'www.google.gp',
    'www.google.gr',
    'www.google.com.gt',
    'www.google.gy',
    'www.google.com.hk',
    'www.google.hn',
    'www.google.hr',
    'www.google.ht',
    'www.google.hu',
    'www.google.co.id',
    'www.google.ie',
    'www.google.co.il',
    'www.google.im',
    'www.google.co.in',
    'www.google.iq',
    'www.google.is',
    'www.google.it',
    'www.google.je',
    'www.google.com.jm',
    'www.google.jo',
    'www.google.co.jp',
    'www.google.co.ke',
    'www.google.com.kh',
    'www.google.ki',
    'www.google.kg',
    'www.google.co.kr',
    'www.google.com.kw',
    'www.google.kz',
    'www.google.la',
    'www.google.com.lb',
    'www.google.li',
    'www.google.lk',
    'www.google.co.ls',
    'www.google.lt',
    'www.google.lu',
    'www.google.lv',
    'www.google.com.ly',
    'www.google.co.ma',
    'www.google.md',
    'www.google.me',
    'www.google.mg',
    'www.google.mk',
    'www.google.ml',
    'www.google.mn',
    'www.google.ms',
    'www.google.com.mt',
    'www.google.mu',
    'www.google.mv',
    'www.google.mw',
    'www.google.com.mx',
    'www.google.com.my',
    'www.google.co.mz',
    'www.google.com.na',
    'www.google.com.nf',
    'www.google.com.ng',
    'www.google.com.ni',
    'www.google.ne',
    'www.google.nl',
    'www.google.no',
    'www.google.com.np',
    'www.google.nr',
    'www.google.nu',
    'www.google.co.nz',
    'www.google.com.om',
    'www.google.com.pa',
    'www.google.com.pe',
    'www.google.com.ph',
    'www.google.com.pk',
    'www.google.pl',
    'www.google.pn',
    'www.google.com.pr',
    'www.google.ps',
    'www.google.pt',
    'www.google.com.py',
    'www.google.com.qa',
    'www.google.ro',
    'www.google.ru',
    'www.google.rw',
    'www.google.com.sa',
    'www.google.com.sb',
    'www.google.sc',
    'www.google.se',
    'www.google.com.sg',
    'www.google.sh',
    'www.google.si',
    'www.google.sk',
    'www.google.com.sl',
    'www.google.sn',
    'www.google.so',
    'www.google.sm',
    'www.google.st',
    'www.google.com.sv',
    'www.google.td',
    'www.google.tg',
    'www.google.co.th',
    'www.google.com.tj',
    'www.google.tk',
    'www.google.tl',
    'www.google.tm',
    'www.google.tn',
    'www.google.to',
    'www.google.com.tr',
    'www.google.tt',
    'www.google.com.tw',
    'www.google.co.tz',
    'www.google.com.ua',
    'www.google.co.ug',
    'www.google.co.uk',
    'www.google.com.uy',
    'www.google.co.uz',
    'www.google.com.vc',
    'www.google.co.ve',
    'www.google.vg',
    'www.google.co.vi',
    'www.google.com.vn',
    'www.google.vu',
    'www.google.ws',
    'www.google.rs',
    'www.google.co.za',
    'www.google.co.zm',
    'www.google.co.zw',
    'www.google.cat',
    'www.google.xxx',
]


def reply(
    message, text, preview=True, fix_markdown=False, delete_orig=False, parse='md'
):
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        ret = message.reply_text(
            text.strip(), disable_web_page_preview=not preview, parse_mode=parse
        )
        if delete_orig:
            message.delete()
        return ret
    except BaseException:
        pass


def extract_args(message, markdown=True):
    if not (message.text or message.caption):
        return ''

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if ' ' not in text:
        return ''

    text = sub(r'\s+', ' ', text)
    text = text[text.find(' ') :].strip()
    return text


def extract_args_arr(message, markdown=True):
    return extract_args(message, markdown).split()


def edit(message, text, preview=True, fix_markdown=False, parse='md'):
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        if message.from_user.id != TEMP_SETTINGS['ME'].id:
            reply(message, text, preview=preview, parse=parse)
            return
        message.edit_text(
            text.strip(), disable_web_page_preview=not preview, parse_mode=parse
        )
    except BaseException:
        pass


def download_media(client, data, file_name=None, progress=None, sticker_orig=True):
    if not file_name:
        if data.document:
            file_name = (
                data.document.file_name
                if data.document.file_name
                else f'{data.document.file_id}.bin'
            )
        elif data.audio:
            file_name = (
                data.audio.file_name
                if data.audio.file_name
                else f'{data.audio.file_id}.mp3'
            )
        elif data.photo:
            file_name = f'{data.photo.file_id}.png'
        elif data.voice:
            file_name = f'{data.voice.file_id}.ogg'
        elif data.video:
            file_name = (
                data.video.file_name
                if data.video.file_name
                else f'{data.video.file_id}.mp4'
            )
        elif data.animation:
            file_name = f'{data.animation.file_id}.mp4'
        elif data.video_note:
            file_name = f'{data.video_note.file_id}.mp4'
        elif data.sticker:
            file_name = f'sticker.{("tgs" if sticker_orig else "json.gz") if data.sticker.is_animated else "webm" if data.sticker.is_video else "webp" if sticker_orig else "png"}'
        else:
            return None

    if progress:
        return client.download_media(data, file_name=file_name, progress=progress)

    return client.download_media(data, file_name=file_name)


def download_media_wc(data, file_name=None, progress=None, sticker_orig=False):
    return download_media(app, data, file_name, progress, sticker_orig)


def get_me():
    return app.get_me()


def forward(message, chat_id):
    try:
        return message.forward(chat_id or 'me')
    except Exception as e:
        raise e


def get_messages(chat_id, msg_ids=None, client=app):
    try:
        ret = client.get_messages(chat_id=(chat_id or 'me'), message_ids=msg_ids)
        return [ret] if ret and isinstance(ret, Message) else ret
    except BaseException:
        return []


def amisudo():
    return TEMP_SETTINGS['ME'].id in BRAIN


def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return amisudo() or SPAM_COUNT[0] < 50


def get_cmd(message):
    text = message.text or message.caption
    if text:
        text = text.strip()
        return parse_cmd(text)
    return ''


def parse_cmd(text):
    cmd = sub(r'\s+', ' ', text)
    cmd = cmd.split()[0]
    cmd = cmd.split(_parsed_prefix)[-1] if BOT_PREFIX else cmd[1:]
    return cmd


def is_admin(message):
    if not 'group' in message.chat.type:
        return True

    user = app.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return user.status in _admin_status_list


def is_admin_myself(chat):
    if not 'group' in chat.type:
        return True

    user = app.get_chat_member(chat_id=chat.id, user_id='me')
    return user.status in _admin_status_list


def get_download_dir() -> str:
    dir = './downloads'
    makedirs(dir, exist_ok=True)
    return dir


def get_duration(media):
    out = __status_out__(
        f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{media}"'
    )
    if LOG_VERBOSE:
        print(out)
    if out[0] == 0:
        return int(float(out[1]))
    return None


def __status_out__(cmd, encoding='utf-8'):
    try:
        output = check_output(
            cmd, shell=True, text=True, stderr=STDOUT, encoding=encoding
        )
        return (0, output)
    except CalledProcessError as ex:
        return (ex.returncode, ex.output)
    except BaseException as e:
        if encoding != 'latin-1':
            return __status_out__(cmd, 'latin-1')
        raise e
