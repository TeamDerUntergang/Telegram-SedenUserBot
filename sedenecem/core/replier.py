# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove, path

from pyrogram.types import Message

from .misc import MARKDOWN_FIX_CHAR, get_duration, __status_out__
from sedenbot import LOG_VERBOSE


def reply_img(
    message,
    photo,
    caption='',
    fix_markdown=False,
    delete_orig=False,
    delete_file=False,
    parse='md',
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        message.reply_photo(photo, caption=caption.strip(), parse_mode=parse)
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
    duration=None,
    fix_markdown=False,
    delete_orig=False,
    delete_file=False,
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR

        if not duration:
            duration = get_duration(audio)

        message.reply_audio(audio, caption=caption.strip(), duration=int(duration))
        if delete_orig:
            message.delete()
        if delete_file:
            remove(audio)
    except BaseException:
        pass


def reply_video(
    message,
    video,
    caption='',
    duration='',
    thumb=None,
    fix_markdown=False,
    progress=None,
    delete_orig=False,
    delete_file=False,
    parse='md',
):
    try:
        if not thumb:
            thumb = 'downloads/thumb.png'
            if path.exists(thumb):
                remove(thumb)
            out = __status_out__(
                f'ffmpeg -i {video} -ss 00:00:01.000 -vframes 1 {thumb}'
            )
            if LOG_VERBOSE:
                print(out)
            if out[0] != 0:
                thumb = None

        if not duration:
            duration = get_duration(video)

        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        if not duration:
            message.reply_video(
                video,
                caption=caption.strip(),
                parse_mode=parse,
                thumb=thumb,
                progress=progress,
            )
        else:
            message.reply_video(
                video,
                caption=caption.strip(),
                duration=int(duration),
                parse_mode=parse,
                thumb=thumb,
                progress=progress,
            )
        if delete_orig:
            message.delete()
        if delete_file:
            remove(video)
    except BaseException as e:
        raise e
        pass


def reply_voice(
    message,
    voice,
    caption='',
    duration=None,
    fix_markdown=False,
    delete_orig=False,
    delete_file=False,
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR

        if not duration:
            duration = get_duration(voice)

        message.reply_voice(voice, caption=caption.strip(), duration=duration)
        if delete_orig:
            message.delete()
        if delete_file:
            remove(voice)
    except BaseException:
        pass


def reply_doc(
    message,
    doc,
    caption='',
    fix_markdown=False,
    delete_orig=False,
    progress=None,
    delete_after_send=False,
):
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


def reply_sticker(message, sticker, delete_orig=False, delete_file=False):
    try:
        message.reply_sticker(sticker)
        if delete_orig:
            message.delete()
        if delete_file:
            remove(sticker)
    except BaseException:
        pass


def reply_msg(message: Message, message2: Message, delete_orig=False):
    try:
        message2.copy(chat_id=message.chat.id, reply_to_message_id=message.message_id)

        if delete_orig:
            message.delete()
    except Exception as e:
        raise e
