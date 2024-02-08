# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove
from time import sleep

from sedenbot import CONVERSATION, app


class PyroConversation:
    """
    A context manager for a conversation with a specific chat ID.

    Args:
        message (pyrogram.types.Message): The original message that initiated the conversation.
        chat_id (int): The ID of the chat with which the conversation is taking place.

    Methods:
        send_msg(text: str) -> None:
            Sends a message to the chat.

        send_doc(doc: str, delete: bool = False) -> None:
            Sends a document to the chat.

        recv_msg(read: bool = True) -> pyrogram.types.Message:
            Receives a message from the chat.

        forward_msg(msg: pyrogram.types.Message) -> pyrogram.types.Message:
            Forwards a message to the chat.

        init() -> None:
            Initializes the conversation.

        stop() -> None:
            Ends the conversation.

    Usage:
        with PyroConversation(message, chat_id) as conv:
            conv.send_msg("Hello!")
            reply = conv.recv_msg()
    """

    def __init__(self, message, chat_id):
        self.client = message._client or app
        self.chat_id = chat_id
        self.count = 0

    def send_msg(self, text):
        self.client.send_message(self.chat_id, text)

    def send_doc(self, doc, delete=False):
        self.client.send_document(self.chat_id, doc)
        if delete:
            remove(doc)

    def recv_msg(self, read=True):
        conv = CONVERSATION[self.chat_id]
        count = 0
        while len(conv) == self.count and count < 100:
            count += 1
            sleep(0.2)

        if count > 99:
            raise Exception

        msg = conv[self.count]
        self.count = len(conv)
        if read:
            self.client.read_chat_history(chat_id=self.chat_id)
        return msg

    def forward_msg(self, msg):
        return msg.forward(self.chat_id)

    def init(self):
        CONVERSATION[self.chat_id] = []

    def stop(self):
        CONVERSATION[self.chat_id] = None

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, a, b, c):
        self.stop()
