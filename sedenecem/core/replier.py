# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import path, remove

from pyrogram import enums
from pyrogram.types import Message

from sedenbot import LOG_VERBOSE

from .misc import MARKDOWN_FIX_CHAR, get_download_dir, get_duration, get_status_out


def reply_img(
    message,
    photo,
    caption='',
    fix_markdown=False,
    delete_orig=False,
    delete_file=False,
    parse=enums.ParseMode.MARKDOWN,
):
    """
    Replies to a given message with a photo and caption.

    Args:
        message (pyrogram.types.Message): The message to reply to.
        photo (str): The path to the photo file to send.
        caption (str): The caption for the photo.
        fix_markdown (bool): Whether to fix markdown issues in the caption.
        delete_orig (bool): Whether to delete the original message after replying.
        delete_file (bool): Whether to delete the photo file after sending.
        parse (pyrogram.enums.ParseMode): The parse mode to use for the caption. Defaults to `pyrogram.enums.ParseMode.MARKDOWN`.
    """
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
    """
    Reply to the given message with the given audio file and caption.

    Args:
        message (pyrogram.types.Message): The message to reply to.
        audio (str): The path to the audio file to send.
        caption (str): The caption to send with the audio file.
        duration (int): The duration of the audio file, in seconds. If not provided, the function will attempt to determine the duration automatically.
        fix_markdown (bool): Whether to fix any issues with the Markdown in the caption. Defaults to False.
        delete_orig (bool): Whether to delete the original message after sending the reply. Defaults to False.
        delete_file (bool): Whether to delete the audio file after sending the reply. Defaults to False.
    """
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
    parse=enums.ParseMode.MARKDOWN,
):
    """
    Reply to message with a video file.

    Args:
        message (pyrogram.types.Message): The message object to reply to.
        video (str): The path to the video file to send.
        caption (str): The caption to attach to the video. Defaults to ''.
        duration (str): The duration of the video in seconds. If not specified, it will be calculated automatically.
        thumb (str): The path to a thumbnail image to attach to the video. If not specified, a thumbnail will be automatically generated from the video. Defaults to None.
        fix_markdown (bool): If True, fix any markdown formatting issues in the caption. Defaults to False.
        progress (callable, optional): A callback function to report the progress of the upload. Defaults to None.
        delete_orig (bool): If True, delete the original message that the reply is being sent to. Defaults to False.
        delete_file (bool): If True, delete the video file after sending it. Defaults to False.
        parse (pyrogram.enums.ParseMode): The parse mode to use for the caption. Defaults to `pyrogram.enums.ParseMode.MARKDOWN`.
    """
    try:
        if not thumb:
            thumb = f'{get_download_dir()}/thumb.png'
            if path.exists(thumb):
                remove(thumb)
            out = get_status_out(
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
    except BaseException:
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
    """
    Reply to message with a voice message.

    Args:
        message (pyrogram.types.Message): The message object to reply to.
        voice (str): The path to the voice message file to send.
        caption (str): The caption to attach to the voice message.
        duration (int): The duration of the voice message in seconds. If not specified, it will be calculated automatically. Defaults to None.
        fix_markdown (bool): If True, fix any markdown formatting issues in the caption. Defaults to False.
        delete_orig (bool): If True, delete the original message that the reply is being sent to. Defaults to False.
        delete_file (bool): If True, delete the voice message file after sending it. Defaults to False.
    """
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
    """
    Reply to message with a document or a media group of documents.

    Args:
        message (pyrogram.types.Message): The message object to reply to.
        doc (Union[str, List[pyrogram.types.Document]]): The document or media group of documents to send.
        caption (str): The caption to attach to the document.
        fix_markdown (bool): If True, fix any markdown formatting issues in the caption. Defaults to False.
        delete_orig (bool): If True, delete the original message that the reply is being sent to. Defaults to False.
        progress (callable, optional): A callback function that will be called with the number of bytes uploaded as an argument. Defaults to None.
        delete_after_send (bool): If True, delete the document file(s) after sending. Defaults to False.
    """
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
    """
    Reply to message with a sticker.

    Args:
        message (pyrogram.types.Message): The message object to reply to.
        sticker (str): The file path of the sticker to send.
        delete_orig (bool): If True, delete the original message that the reply is being sent to. Defaults to False.
        delete_file (bool): If True, delete the sticker file after sending. Defaults to False.
    """
    try:
        message.reply_sticker(sticker)
        if delete_orig:
            message.delete()
        if delete_file:
            remove(sticker)
    except BaseException:
        pass


def reply_msg(message: Message, message2: Message, delete_orig=False):
    """
    Reply to message with another message.

    Args:
        message (pyrogram.types.Message): The original message object to reply to.
        message2 (pyrogram.types.Message): The message object to send as the reply.
        delete_orig (bool): If True, delete the original message that the reply is being sent to. Defaults to False.
    """
    try:
        message2.copy(chat_id=message.chat.id, reply_to_message_id=message.id)

        if delete_orig:
            message.delete()
    except Exception as e:
        raise e
