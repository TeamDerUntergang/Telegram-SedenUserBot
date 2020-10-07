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

from re import escape, sub
from pyrogram import Message
from sedenbot import app, me, BRAIN_CHECKER, BOT_PREFIX

MARKDOWN_FIX_CHAR = '\u2064'
SPAM_COUNT = [0]
_parsed_prefix = escape(BOT_PREFIX or '.')


def extract_args(message, markdown=True):
    text = message.text.markdown if markdown else message.text
    if ' ' not in text:
        return ''

    text = sub(r'\s+', ' ', text)
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
        message.edit_text(
            text.strip(),
            disable_web_page_preview=not preview,
            parse_mode=parse)
    except BaseException:
        pass


def download_media(
        client,
        data,
        file_name=None,
        progress=None,
        sticker_orig=False):
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
            file_name = f'{data.sticker.file_name}.{"TGS" if data.sticker.is_animated else ("webp" if sticker_orig else "png")}'
        else:
            return None

    if progress:
        return client.download_media(
            data, file_name=file_name, progress=progress)

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
        return None


def get_messages(chat_id, msg_ids=None, client=app):
    try:
        ret = client.get_messages(
            chat_id=(chat_id or 'me'), message_ids=msg_ids)
        return [ret] if ret and isinstance(ret, Message) else ret
    except BaseException:
        return []


def amisudo():
    return me[0].id in BRAIN_CHECKER


def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return amisudo() or SPAM_COUNT[0] < 50


def get_cmd(message):
    if message.text:
        text = message.text.strip()
        return parse_cmd(text)
    return ''


def parse_cmd(text):
    return (text[len(_parsed_prefix):text.find(' ')]
            if ' ' in text else text[len(_parsed_prefix):]).strip()
