# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove

from .misc import MARKDOWN_FIX_CHAR, download_media_wc


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
    duration='',
    fix_markdown=False,
    delete_orig=False,
    delete_file=False,
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        if not duration:
            message.reply_audio(audio, caption=caption.strip())
        else:
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
    delete_orig=False,
    delete_file=False,
    parse='md',
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        if not duration:
            message.reply_video(
                video, caption=caption.strip(), parse_mode=parse, thumb=thumb
            )
        else:
            message.reply_video(
                video,
                caption=caption.strip(),
                duration=int(duration),
                parse_mode=parse,
                thumb=thumb,
            )
        if delete_orig:
            message.delete()
        if delete_file:
            remove(video)
    except BaseException:
        pass


def reply_voice(
    message, voice, caption='', fix_markdown=False, delete_orig=False, delete_file=False
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        message.reply_voice(voice, caption=caption.strip())
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
