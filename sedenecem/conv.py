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

from pyrogram import Filters, MessageHandler
from sedenbot import CONVERSATION
from time import sleep
from os import remove


class PyroConversation:

    def __init__(self, client, chat_id):
        self.client = client or app
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
            self.client.read_history(chat_id=self.chat_id)
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
