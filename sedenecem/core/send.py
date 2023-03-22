# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from pyrogram.types import Chat

from .misc import MARKDOWN_FIX_CHAR


def send(client, chat, text, fix_markdown=False, reply_id=None):
    """
    Sends a message to the specified chat. If the message is too long, it is sent as a document.

    Args:
        client (pyrogram.Client): The client used to send the message.
        chat (Union[pyrogram.types.Chat, int, str]): The ID, username, or `Chat` object of the chat to send the message to.
        text (str): The text of the message to send.
        fix_markdown (bool): Whether to fix the markdown of the message. Defaults to False.
        reply_id (int): The ID of the message to reply to. Defaults to None.
    """
    if fix_markdown:
        text += MARKDOWN_FIX_CHAR

    if len(text) < 4096:
        if not reply_id:
            client.send_message(chat.id if isinstance(chat, Chat) else chat, text)
        else:
            client.send_message(
                chat.id if isinstance(chat, Chat) else chat,
                text,
                reply_to_message_id=reply_id,
            )
        return

    file = open('temp.txt', 'w+')
    file.write(text)
    file.close()
    send_doc(client, chat, 'temp.txt')


def send_sticker(message, chat, sticker):
    """
    Sends a sticker to the specified chat.

    Args:
        message (pyrogram.types.Message): The original message object that the sticker is being sent in reply to.
        chat (Union[pyrogram.types.Chat, int, str]): The ID, username, or `Chat` object of the chat to send the sticker to.
        sticker (Union[pyrogram.types.Sticker, str]): The `Sticker` object or file ID of the sticker to send.
    """
    try:
        message._client.send_sticker(
            chat.id if isinstance(chat, Chat) else chat, sticker
        )
    except BaseException:
        pass


def send_doc(client, chat, doc, caption='', fix_markdown=False):
    """
    Sends a document to the specified chat.
    
    Args:
        client (pyrogram.Client): The client used to send the message.
        chat (Union[pyrogram.types.Chat, int, str]): The ID, username, or `Chat` object of the chat to send the document to.
        doc (str): The file path of the document to send.
        caption (str): The caption of the document. Defaults to an empty string.
        fix_markdown (bool): If True, the caption will be appended with a markdown fix character. Defaults to False.
    """
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        client.send_document(
            chat.id if isinstance(chat, Chat) else chat, doc, caption=caption
        )
    except BaseException:
        pass
