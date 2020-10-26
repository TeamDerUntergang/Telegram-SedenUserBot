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

from os import remove
from .misc import MARKDOWN_FIX_CHAR, download_media_wc, reply


def reply_img(
        message,
        photo,
        caption='',
        fix_markdown=False,
        delete_orig=False,
        delete_file=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        message.reply_photo(photo, caption=caption.strip())
        if delete_orig:
            message.delete()

        if delete_file:
            remove(photo)
    except BaseException:
        pass


def reply_audio(
        message,
        audio,
        caption='',
        fix_markdown=False,
        delete_orig=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        message.reply_audio(audio, caption=caption.strip())
        if delete_orig:
            message.delete()
    except BaseException:
        pass


def reply_voice(
        message,
        voice,
        caption='',
        fix_markdown=False,
        delete_orig=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        message.reply_voice(voice, caption=caption.strip())
        if delete_orig:
            message.delete()
    except BaseException:
        pass


def reply_doc(
        message,
        doc,
        caption='',
        fix_markdown=False,
        delete_orig=False,
        progress=None,
        delete_after_send=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        if isinstance(doc, str):
            message.reply_document(
                doc, caption=caption.strip(), progress=progress)
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
    except BaseException:
        pass


def reply_msg(message, message2, delete_orig=False):
    try:
        filename = None
        if message2.media:
            filename = download_media_wc(message2, sticker_orig=True)
            if message2.audio:
                message.reply_audio(filename)
            elif message2.animation:
                message.reply_animation(filename)
            elif message2.sticker:
                message.reply_sticker(filename)
            elif message2.photo:
                message.reply_photo(filename)
            elif message2.video:
                message.reply_video(filename)
            elif message2.voice:
                message.reply_voice(filename)
            elif message2.video_note:
                message.reply_video_note(filename)
            elif message2.document:
                message.reply_document(filename)
            else:
                filename = None
                message2.forward(message.chat.id)

            if filename:
                remove(filename)
        else:
            message.reply_text(message2.text)

        if delete_orig:
            message.delete()
    except Exception as e:
        raise e
